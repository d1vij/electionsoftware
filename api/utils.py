import hashlib
import time
import os
import chalk

from .models import VoteResponse


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


# totally not leaked database info here
CONNECTIONSTRING = "mongodb+srv://vermadivij:databasepassword@cluster1.lzjrylx.mongodb.net/?retryWrites=true&w=majority&appName=cluster1"
URL = ""
PORT = None


# Name of database used in cluster
DATABASE_NAME = "voting"

# Name of collection used to store all the votes
ACTIVE_COLLECTION = "votes1"

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
    def warning(message: str):
        print(chalk.red.bold(f"[X] {str}"))

    @classmethod
    def success(message: str):
        print(chalk.green(f"[✓] {message}"))

    @classmethod
    def info(message: str):
        print(chalk.blue(f"[*] {message}"))


