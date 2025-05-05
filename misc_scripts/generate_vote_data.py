import random
import os
import sys
import pymongo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from utils import candidate_data, CONNECTIONSTRING,DATABASE_NAME,collection,generate_token # type: ignore

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
    post_data(generate_data(int(input("Count of fake vote sessions : "))))