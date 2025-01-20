#logs vote to file
import csv
from datetime import datetime


filename = "votes.csv"

EOL = lambda : print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

def log(candidate : str, post : str):
    with open(filename, mode = "a+", encoding = "utf-8", ) as file:
        writer = csv.writer(file)
        time_ : str = datetime.now().strftime("%I:%M %p  %d-%M-%Y")
        content = [candidate, post, time_]
        writer.writerow(content)


def see_votes():
    vote_count: dict[(str, str) : int] = {}

    def counter(data : tuple[str, str]) :
        #data = (name, post)
        if data in vote_count.keys() :
            vote_count[data] += 1
        else :
            vote_count[data] = 1

    with open("votes.csv", "r", encoding = 'utf-8', newline = '\n') as file :
        reader_ = csv.reader(file)

        for row in reader_ :
            t = (row[0], row[1])  # name and post resp
            counter(t)

    for (name, post), count in vote_count.items() :
        print(f"{name} got voted for the post {post} : {count} times")