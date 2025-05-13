import hashlib
import time
import os
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from .models import VoteResponse

candidate_data = {
    "head_boy" : ["Divij", "Rohan", "Aditya", "Karan", "Nishant"],
    "head_girl" : ["Aisha", "Shruti", "Meera", "Anita", "Priya"],
    "sports_captain" : ["Rahul", "Arjun", "Vivek", "Kavya", "Tarun"],
    "cultural_secretary" : ["Neha", "Tanya", "Tina", "Mira", "Rhea"],
    "discipline_incharge" : ["Naman", "Simran", "Raj", "Rehan", "Bhavya"],
    "tech_leader" : ["Zoya", "Sid", "Manav", "Kabir", "Hardik"],
    "eco_head" : ["Isha", "Dev", "Parth", "Veer", "Lavanya"],
    "media_incharge" : ["Mehul", "Anaya", "Krishna", "Sarthak", "Niharika"]
}   

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "..", "public/html")
MAIN_HTML_PATH = os.path.join(SRC_PATH, "main.html")

# print(SRC_PATH, MAIN_HTML_PATH)

origins = ["*"]

#totally not leaked database info here
CONNECTIONSTRING = "mongodb+srv://vermadivij:databasepassword@cluster1.lzjrylx.mongodb.net/?retryWrites=true&w=majority&appName=cluster1"
URL = ""
PORT = None

DATABASE_NAME = "voting"
collection = "votes1"


def generate_token() -> str:
    """retuns a token / sha256 hashed string based on time of call"""
    return hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()

def Message(t: str) -> dict :
    return {"message" : t}



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
    
    async def fetchResults(self,*,collection:str) -> list[VoteResponse]:
        collection :AsyncIOMotorCollection= self.database[collection]

        cursor =  collection.find()
        return await cursor.to_list()