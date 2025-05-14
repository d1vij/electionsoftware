import random
import pymongo

from utils import *

client = pymongo.MongoClient(CONNECTIONSTRING)
working_database = client[DATABASE_NAME]
working_collection = working_database[ACTIVE_COLLECTION]


def generate_data(data_count):
    l = []
    for _ in range(data_count):
        t = generate_token()
        vd = []
        posts = list(candidate_data.keys())
        for p in posts:
            c = random.choice(candidate_data.get(p))
            vd.append({"name": c, "post": p})
        e = {"token": t, "vote_data": vd}
        l.append(e)
    print("generated data")
    return l


def post_data(data):
    """posts dummy vote data"""
    working_collection.insert_many(data)
    print("uploaded data")


def DELETE_ALL():
    working_collection.delete_many({})


if __name__ == "__main__":
    o = input("what 1.fakevotes 2.deletevotes-PLEASEDELETEVOTES")
    match o:
        case "fakevotes":
            post_data(generate_data(
                int(input("Count of fake vote sessions : "))))
        case "PLEASEDELETEVOTES":
            DELETE_ALL()
        case _: print("invalid ", o)
