"""
Main uris 
-> /voteapp
-> /results

"""
from uuid import uuid4

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .utilities.utils import SRC_PATH
from .utilities.utils import origins
from .utilities.utils import Log
from .utilities.utils import CONNECTIONSTRING, DATABASE_NAME, ACTIVE_COLLECTION

from .utilities.results import getResultGraphs
from .utilities.models import VoteResponse
from .utilities.database_wrapper import DatabaseWrapper


#Loading env variables


if CONNECTIONSTRING in ["", None]: exit("CONNECTION STRING WAS NOT SET IN UTILS.py!!!")

connObj = DatabaseWrapper(
    connection_string=CONNECTIONSTRING,
    database=DATABASE_NAME
)




class API:
    def __init__(self):
        self.app = FastAPI()
        self.app.mount("/public",StaticFiles(directory=SRC_PATH),name="public")

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
            """no vote processing occurs here, anything coming from client is directly inserting into database"""

            # model_dump method converts the incoming form data to VoteResponse formatted dict
            insertionStatus = await self.connection.add_to_collection(collection=ACTIVE_COLLECTION, data=request.model_dump())

            Log.info(request.model_dump())
            if insertionStatus==True:
                return {"status": "success"}
            else:
                Log.warning("Error in inserting votes")
                return {"status": "Error in votes upload, call for help"}

    def get_routes(self):

        @self.app.get('/result-images')
        async def get_result_images():
            """helper function to request graphs"""
            return {"imagedata": await getResultGraphs()}

        @self.app.get('/results')
        async def get_result_page():
            """loads result page"""
            return RedirectResponse("/public/html/results.html")

        @self.app.get("/gettoken")
        async def get_token():
            """retuns unique uuid through which voting sessions could be tracked"""
            return {"token": uuid4()}

        @self.app.get('/voteapp')
        async def get_vote_html():
            """main voting app uri"""
            return RedirectResponse("/public/html/main.html")

        @self.app.get('/')
        async def _():
            return RedirectResponse("/voteapp")



app = API().app
