from fastapi import FastAPI, Request # main fastapi class
from fastapi.responses import HTMLResponse # class to return html as response
from fastapi.staticfiles import StaticFiles #serving static files along with html
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection

from .utils import CONNECTIONSTRING
from .utils import DATABASE_NAME
from .utils import URL
from .utils import PORT
from .utils import SRC_PATH
from .utils import MAIN_HTML_PATH
from .utils import candidate_data
from .utils import Message
from .utils import generate_token
from .utils import origins
from .utils import Connection

from .models import VoteResponse

import aiofiles
import io
import base64
import asyncio
import os

# debug
from pprint import pprint
import matplotlib.pyplot as plt

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC_PATH, "main.html")
with open(file_path, mode = "r") as file :
    MAIN_FILE =  HTMLResponse(content = file.read())

connObj = Connection(
                connection_string = CONNECTIONSTRING,
                url=URL,
                port=PORT,
                database = DATABASE_NAME
        )





async def makeGraph(post, vote_dict) -> str:
    # Sort by vote count (descending)
    sorted_items = sorted(vote_dict.items(), key = lambda x : x[1], reverse = True)
    names, counts = zip(*sorted_items)
    plt.figure(figsize = (6, 3.5))
    plt.title(post)
    colors = plt.cm.viridis([i / len(names) for i in range(len(names))])
    bars = plt.bar(names, counts, color = colors)
    plt.grid(axis = 'y', linestyle = '--', alpha = 0.5)
    for bar, count in zip(bars, counts) :
        yval = bar.get_height()
        plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval + max(counts) * 0.015,  # slight vertical offset
                str(count),
                ha = 'center', va = 'bottom',
                fontsize = 8, color = 'black'
        )
    min_y = min(counts)
    plt.ylim(min_y - 20, max(counts) + 40)
    plt.tight_layout()

    buffer = io.BytesIO()
    
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    
    # plt.close() # this here causes 
    return f"data:image/png;base64,{base64.b64encode(buffer.read()).decode('utf-8')}"

async def getResultGraphs() -> list[str]:
    #TODO:REFACTOR
    results:list[VoteResponse] = await connObj.fetchResults(collection="votes1")
    posts = {p : dict.fromkeys(candidate_data[p], 0) for p in candidate_data.keys()}

    # print(results[0])
    # print(posts)

    seen_tokens =[]
    #updating votes from results
    for i,document in enumerate(results):
        print(i)
        if not (document["token"] in seen_tokens):
            seen_tokens.append(document['token'])
            for vote in document['vote_data']:
                try :
                    post_name = vote["post"]
                    voted_candidate = vote['name']
                    
                    curPostCandidates = posts[post_name]
                    # print(curPostCandidates)
    
                    curPostCandidates[voted_candidate] += 1
                except Exception as e:
                    # temporatry 
                    pass            

                
    #making graphs
    img_data = await asyncio.gather(*[makeGraph(post, vote_dict) for post,vote_dict in posts.items()])

    return img_data
    



class API:
    def __init__(self):
        self.app = FastAPI()
        self.app.mount("/public",
                       StaticFiles(directory = SRC_PATH), #js html css in src_path
                       name = "public")

        self.app.add_middleware(
                CORSMiddleware, #type: ignore
                allow_origins = origins,
                allow_credentials = False,
                allow_methods = ["*"],
                allow_headers = ["*"],
        )

        self.connection = connObj

        # initializing routes
        self.get_routes()
        self.post_routes()

    def post_routes(self):

        @self.app.post("/submitvotes")
        async def post_votes(request :VoteResponse) :
            s = await self.connection.add_to_collection(collection="votes1",data=request.model_dump()) #model_dump method converts the incoming form data to VoteResponse formatted dict
            # TODO: add some better response
            if s:
                return {"status":"success"}
            else: return {"status":"oogieboogie"}



    def get_routes(self):
        @self.app.get('/result-images')
        async def get_result_images():
            return  {"imagedata":await getResultGraphs()}

        @self.app.get('/resultpage', response_class=HTMLResponse)
        async def get_result_page():
            async with aiofiles.open('./public/html/results.html','r',encoding='utf-8') as file:
                return await file.read()

        @self.app.get("/candidates")
        async def get_candidate_data() :
            return candidate_data

        @self.app.get("/gettoken")
        async def get_token():
            t =  generate_token()
            return {"token":t}

        @self.app.get('/voteapp')
        async def get_vote_html() -> HTMLResponse :
            return MAIN_FILE


app = API().app