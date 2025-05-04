import hashlib
import time


candidate_data = {
    "sports_captain_boy" : ['Liam Smith', 'Ava Jones', 'Mason Thomas', 'Harper Anderson', 'Noah Williams',
                          'Evelyn Taylor', 'William Garcia', 'James Davis'],
    "sports_captain_girl" : ['Isabella Rodriguez', 'Ethan Moore', 'Amelia Gonzalez', 'Harper Anderson', 'Sophia Miller',
                           'Elijah Lopez'],
    "head_boy" : ['Charlotte Jackson', 'Emma Johnson', 'Harper Anderson', 'Mason Thomas', 'Mia Hernandez', 'Ethan Moore',
                'Isabella Rodriguez', 'Liam Smith'],
    "head_girl" : ['Liam Smith', 'Mason Thomas', 'Ava Jones', 'Evelyn Taylor']
};

STATIC_PATH="../static"
SRC_PATH="../src"
origins = ["*"]

CONNECTIONSTRING = ""
URL = ""
PORT = None

DATABASE_NAME = ""
collection = ""


def generate_token() -> str:
    """retuns a token / sha256 hashed string based on time of call"""
    return hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()

def Message(t: str) -> dict :
    return {"message" : t}