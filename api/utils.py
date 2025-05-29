import hashlib
import time
import os
import chalk
import random
import pymongo


"""Change candidate data here
NOTE: Candidate names are CASE SENSITIVE
"""
candidate_data = {
    "head_boy": ["Divij", "Rohan", "Aditya", "Karan", "Nishant"],
    "head_girl": ["Aisha", "Shruti", "Meera", "Anita", "Priya"],
    "sports_captain": ["Rahul", "Arjun", "Vivek", "Kavya", "Tarun"],
    "cultural_secretary": ["Neha", "Tanya", "Tina", "Mira", "Rhea"],
    "discipline_incharge": ["Naman", "Simran", "Raj", "Rehan", "Bhavya"],
    "tech_leader": ["Zoya", "Sid", "Manav", "Kabir", "Hardik"],
    "eco_head": ["Isha", "Dev", "Parth", "Veer", "Lavanya"],
    "media_incharge": ["Mehul", "Anaya", "Krishna", "Sarthak", "Niharika"]
}



CONNECTIONSTRING = "mongodb+srv://vermadivij:databasepassword@cluster1.lzjrylx.mongodb.net/?retryWrites=true&w=majority&appName=cluster1" # ADD CONNNECTION STRING HERE
URL = ""
PORT = None


# Name of database used in cluster
DATABASE_NAME = "voting"

# Name of collection used to store all the votes
ACTIVE_COLLECTION = "votes"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Source path -> js, css
SRC_PATH = os.path.join(BASE_DIR, "..", "public")

# Vote app file path
MAIN_HTML_PATH = os.path.join(SRC_PATH, "html", "main.html")
print(f"{SRC_PATH=}, {MAIN_HTML_PATH=}")


# Allowed CORS origins
origins = ["*"]


def generate_token() -> str:
    """retuns a token / sha256 hashed string based on time of call"""
    return hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()


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
