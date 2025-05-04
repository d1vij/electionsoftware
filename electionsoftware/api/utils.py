import hashlib
import time
import os


candidate_data = {
    "sports_captain_boy" : ['Liam Smith', 'Ava Jones', 'Mason Thomas', 'Harper Anderson', 'Noah Williams',
                          'Evelyn Taylor', 'William Garcia', 'James Davis'],
    "sports_captain_girl" : ['Isabella Rodriguez', 'Ethan Moore', 'Amelia Gonzalez', 'Harper Anderson', 'Sophia Miller',
                           'Elijah Lopez'],
    "head_boy" : ['Charlotte Jackson', 'Emma Johnson', 'Harper Anderson', 'Mason Thomas', 'Mia Hernandez', 'Ethan Moore',
                'Isabella Rodriguez', 'Liam Smith'],
    "head_girl" : ['Liam Smith', 'Mason Thomas', 'Ava Jones', 'Evelyn Taylor']
}   

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(BASE_DIR, "..", "public")
MAIN_HTML_PATH = os.path.join(SRC_PATH, "main.html")

# print(SRC_PATH, MAIN_HTML_PATH)

origins = ["*"]

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