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
from .models import VoteResponse

import os

# debug
from pprint import pprint

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC_PATH, "main.html")
with open(file_path, mode = "r") as file :
    MAIN_FILE =  HTMLResponse(content = file.read())


class Connection:
    def __init__(self,*,connection_string=None,url=None,port=None,database:str):
        if connection_string:
            self.client = AsyncIOMotorClient(connection_string)
        elif url and port :
            self.client = AsyncIOMotorClient(url, port)

        self.database = self.client.get_database(database)

    async def add_to_collection(self,*,collection:str,data:dict):
        try:
            collection : AsyncIOMotorCollection = self.database.get_collection(collection)
            res = await collection.insert_one(data)
            if res.acknowledged:
                #insertion success
                return True
            else:
                return False
        except Exception as e:
            print(e)

class API:
    def __init__(self):
        self.app = FastAPI()
        self.app.mount("/src",
                       StaticFiles(directory = SRC_PATH),
                       name = "src")

        self.app.add_middleware(
                CORSMiddleware, #type: ignore
                allow_origins = origins,
                allow_credentials = False,
                allow_methods = ["*"],
                allow_headers = ["*"],
        )

        self.connection = Connection(
                connection_string = CONNECTIONSTRING,
                url=URL,
                port=PORT,
                database = DATABASE_NAME
        )

        # initializing routes
        self.get_routes()
        self.post_routes()

    def post_routes(self):

        @self.app.post("/submitvotes")
        async def post_votes(request :VoteResponse) :
            s = await self.connection.add_to_collection(collection="votes1",data=request.model_dump())
            # TODO: add some better response
            if s:
                return {"status":"success"}
            else: return {"status":"oogieboogie"}



    def get_routes(self):

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

