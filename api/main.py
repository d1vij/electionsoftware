"""
Main uris 
-> /voteapp
-> /results

"""


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection

from .utils import DATABASE_NAME
from .utils import CONNECTIONSTRING
from .utils import URL
from .utils import SRC_PATH
from .utils import MAIN_HTML_PATH
from .utils import candidate_data
from .utils import generate_token
from .utils import origins
from .utils import Log
from .utils import ACTIVE_COLLECTION

from .models import VoteResponse

import os
from io import BytesIO
from base64 import b64encode
import asyncio
import aiofiles
from pprint import pprint
import matplotlib.pyplot as plt


with open(MAIN_HTML_PATH, mode="r") as file:
    MAIN_FILE = HTMLResponse(content=file.read())


class DatabaseWrapper:
    """wrapper class for database connections"""

    def __init__(self, *, connection_string=None, url=None, port=None, database: str):
        """Provite either the databse uri/connection string or url and port along with the database name as kwargs"""

        if connection_string:
            self.client = AsyncIOMotorClient(connection_string)
        elif url and port:
            self.client = AsyncIOMotorClient(url, port)
        else:
            Log.warning("INVALID CONNECTION PARAMETERS PROVIDED")
            # raise Exception()


        self.database = self.client.get_database(database)

    async def add_to_collection(self, *, collection: str, data: dict):
        """inserts provided dictionary as it is into provided collection"""
        try:
            _collection: AsyncIOMotorCollection = self.database.get_collection(collection)
            insertion_response = await _collection.insert_one(data)
            if insertion_response.acknowledged:
                # insertion success
                return True
            else:
                return False
        except Exception as e:
            print(e)
            Log.warning(str(e))

    async def fetchResults(self, *, collection: str, query={}) -> list[VoteResponse]:
        """fetches all results as per query, query defaults to {} if nothing provided"""

        _collection: AsyncIOMotorCollection = self.database[collection]
        cursor = _collection.find(query)
        return await cursor.to_list()


connObj = DatabaseWrapper(
    connection_string=CONNECTIONSTRING,
    database=DATABASE_NAME
)


async def makeGraph(post, vote_dict) -> str:
    # Sort by vote count (descending)
    sorted_items = sorted(vote_dict.items(), key=lambda x: x[1], reverse=True)
    names, counts = zip(*sorted_items)
    plt.figure(figsize=(6, 3.5))
    plt.title(post)
    colors = plt.cm.viridis([i / len(names) for i in range(len(names))]) # type: ignore
    bars = plt.bar(names, counts, color=colors)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    for bar, count in zip(bars, counts):
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + max(counts) * 0.015,  # slight vertical offset
            str(count),
            ha='center', va='bottom',
            fontsize=8, color='black'
        )
    min_y = min(counts)
    plt.ylim(min_y - 20, max(counts) + 40)
    plt.tight_layout()

    buffer = BytesIO()

    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # plt.close() # this here causes
    return f"data:image/png;base64,{b64encode(buffer.read()).decode('utf-8')}"


async def getResultGraphs() -> list[str]:
    """
    requests all vote documents and returns array of base64 encoded string of graph image bytes
    -> each graph's string is in format "data:image/png;base64,<b64str>" and the image can be rendered directly in frontend by setting img src to the string
    """

    all_documents: list[VoteResponse] = await connObj.fetchResults(collection=ACTIVE_COLLECTION)
    compiled_results = {p: dict.fromkeys(candidate_data[p], 0) for p in candidate_data.keys()}

    print("Empty results dict")
    pprint(compiled_results,indent=2)

    Log.info(f"Total documents found {len(all_documents)}")

    seen_tokens = []
    document: VoteResponse
    # updating votes from results
    for document in all_documents:
        try:
            token = document['token']              # type: ignore
            if not (token in seen_tokens):
                seen_tokens.append(token)
                for vote in document['vote_data']: # type: ignore
                    try:
                        post_name = vote["post"]
                        voted_candidate = vote['name']
                        curPostCandidates = compiled_results[post_name]
                        curPostCandidates[voted_candidate] += 1
                    except Exception as e:
                        Log.warning(str(e))
        except Exception as e:
            print(document)
            exit()
    img_data = await asyncio.gather(*[makeGraph(post, vote_dict) for post, vote_dict in compiled_results.items()])

    pprint(compiled_results)
    return img_data


class API:
    def __init__(self):
        self.app = FastAPI()
        self.app.mount("/public",
                       StaticFiles(directory=SRC_PATH),  # for css and js
                       name="public")

        self.app.add_middleware(
            CORSMiddleware,  # type: ignore
            allow_origins=origins,  # TODO:Probably restrict origins
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.connection = connObj

        # initializing routes
        self.get_routes()
        self.post_routes()

    def post_routes(self):

        @self.app.post("/submitvotes")
        async def post_votes(request: VoteResponse):
            """no vote processing occurs here, anything coming from client is direclty inserting into database"""

            # model_dump method converts the incoming form data to VoteResponse formatted dict
            insertionStatus = await self.connection.add_to_collection(collection=ACTIVE_COLLECTION, data=request.model_dump())
            Log.info(request.model_dump()) # type: ignore
            if insertionStatus == True:
                return {"status": "success"}
            else:
                Log.warning("Error in inserting votes")
                return {"status": "Error in votes upload, call for help"}

    def get_routes(self):

        @self.app.get('/result-images')
        async def get_result_images():
            """helper function to request graphs"""
            return {"imagedata": await getResultGraphs()}

        @self.app.get('/results', response_class=HTMLResponse)
        async def get_result_page():
            """loads result page"""
            async with aiofiles.open('./public/html/results.html', 'r', encoding='utf-8') as file:
                return await file.read()

        @self.app.get("/getcandidates")
        async def get_candidate_data():
            # NOTE:candidate data could probably just kept in the script
            return candidate_data

        @self.app.get("/gettoken")
        async def get_token():
            """retuns unique token through which voting sessions could be tracked"""
            return {"token": generate_token()}

        @self.app.get('/voteapp')
        async def get_vote_html() -> HTMLResponse:
            """main voting app uri"""
            return MAIN_FILE


if __name__=="__main__":
    app = API().app
