import random
import pymongo
import hashlib
import time
# from utils import *
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
def generate_token() -> str:
    """retuns a token / sha256 hashed string based on time of call"""
    return hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()

CONNECTIONSTRING = "mongodb+srv://vermadivij:databasepassword@cluster1.lzjrylx.mongodb.net/?retryWrites=true&w=majority&appName=cluster1"
DATABASE_NAME = "voting"
collection = "votes1"
client = pymongo.MongoClient(CONNECTIONSTRING)
working_database = client[DATABASE_NAME]
working_collection = working_database[collection]


def generate_data(data_count) :
    l = []
    for _ in range(data_count) :
        t=generate_token()
        vd = []
        posts = list(candidate_data.keys())
        for p in posts :
            c = random.choice(candidate_data.get(p))
            vd.append({"name" : c, "post" : p})
        e = {"token" : t, "vote_data" : vd}
        l.append(e)
    print("generated data")
    return l


def post_data(data) :
    working_collection.insert_many(data)
    print("uploaded data")



def DELETE_ALL() :
    working_collection.delete_many({})

   
if __name__=="__main__":
    o = input("what 1.fakevotes 2.deletevotes-PLEASEDELETEVOTES")
    match o:
        case "fakevotes":
            post_data(generate_data(int(input("Count of fake vote sessions : "))))
        case "PLEASEDELETEVOTES":
            DELETE_ALL()
        case _: print("invalid ",o)