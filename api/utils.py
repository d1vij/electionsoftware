import os
import chalk
import random
import pymongo
import uuid
import json
from pathlib import Path
from dotenv import  load_dotenv
load_dotenv(dotenv_path=Path(".env")) # .env file in the root directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Source path -> js, css
SRC_PATH = os.path.join(BASE_DIR, "..", "public")
CANDIDATE_DATA_PATH = os.path.join(SRC_PATH,"candidate-data")
# Vote app file path
MAIN_HTML_PATH = os.path.join(SRC_PATH, "html", "main.html")
print(f"{SRC_PATH=}, {MAIN_HTML_PATH=}")


# Allowed CORS origins
origins = ["*"]


def generate_token() -> str:
    return uuid.uuid4().__str__()

class Log:
    """simple logging class"""
    @classmethod
    def warning(cls ,message: str):
        print(chalk.red(f"[X] {message}"))

    @classmethod
    def success(cls, message: str):
        print(chalk.green(f"[✓] {message}"))

    @classmethod
    def info(cls, message: str):
        print(chalk.blue(f"[*] {message}"))



def getCandidateDataDict() -> dict[str,list[str]]:
    with open(os.path.join(CANDIDATE_DATA_PATH, "candidates.json"), "r") as file :
        raw = json.loads(file.read())
    parsed = {}
    for post in raw:
        candidates = []
        for candidate in post['candidates']:
            candidates.append(candidate["name"])

        parsed[post["name"]] = candidates


    return parsed

CONNECTIONSTRING = os.getenv("CONNECTION_STRING")
DATABASE_NAME = os.getenv("DATABASE_NAME")
ACTIVE_COLLECTION = os.getenv("ACTIVE_COLLECTION")
print(CONNECTIONSTRING)
candidate_data = getCandidateDataDict()

if __name__ == "__main__":
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
                c = random.choice(candidate_data.get(p)) # type: ignore | shut up pylance
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


    o = input("what 1.fakevotes 2.delete all votes- PLEASEDELETEVOTES >")
    match o:
        case "fakevotes":
            post_data(generate_data(
                int(input("Count of fake vote sessions : "))))
        case "PLEASEDELETEVOTES":
            DELETE_ALL()
            print("Deleted votes")
        case _: print("invalid ", o)
