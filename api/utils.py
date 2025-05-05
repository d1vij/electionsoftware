import hashlib
import time
import os


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
SRC_PATH = os.path.join(BASE_DIR, "..", "public")
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
