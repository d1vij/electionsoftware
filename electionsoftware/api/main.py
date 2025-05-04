from fastapi import FastAPI, Request # main fastapi class
from fastapi.responses import HTMLResponse # class to return html as response
from fastapi.staticfiles import StaticFiles #serving static files along with html
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection

from utils import candidate_data, STATIC_PATH,Message,SRC_PATH,generate_token
from models import VoteResponse

from pprint import pprint

with open('../static/main.html', mode = "r") as file :
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
    def __init__(self,static_directory=STATIC_PATH):
        self.app = FastAPI()
        self.app.mount("/static",StaticFiles(directory=static_directory))
        self.app.mount("/src",StaticFiles(directory=SRC_PATH))
        self.app.add_middleware(
                CORSMiddleware,
                allow_origins = ["*"],
                allow_credentials = False, ########
                allow_methods = ["*"],
                allow_headers = ["*"],
        )

        self.connection = Connection(url = "127.0.0.1",port=27017,database = "votedb")

        self.get_routes()
        self.post_routes()

    def post_routes(self):
        @self.app.post("/submitvotes")
        async def post_votes(request :VoteResponse) :
            s = await self.connection.add_to_collection(collection="votes1",data=request.model_dump())
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

