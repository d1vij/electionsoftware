import pymongo
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
from utils import candidate_data, CONNECTIONSTRING,DATABASE_NAME,collection # type: ignore

client = pymongo.MongoClient(CONNECTIONSTRING)
working_database = client[DATABASE_NAME]
working_collection = working_database[collection]

def make_result_dict() :
    return {p : dict.fromkeys(candidate_data[p], 0) for p in candidate_data.keys()}

def get_results_from_db() :
    print(f"{working_collection.count_documents({}) = }")

    seen_tokens = []
    r = make_result_dict()

    alldocuments = working_collection.find()
    for document in alldocuments :
        token = document['token']
        if not token in seen_tokens :
            seen_tokens.append(token)
            vote_data = document["vote_data"]
            for vote in vote_data :
                post = vote["post"]
                candidate = vote["name"]
                allcandidates = r[post]
                allcandidates[candidate] += 1

    return r


def make_graphs(results: dict[str, dict[str, int]]) :
    for post, vote_dict in results.items() :
        # Sort by vote count (descending)
        sorted_items = sorted(vote_dict.items(), key = lambda x : x[1], reverse = True)
        names, counts = zip(*sorted_items)
        plt.figure(figsize = (6, 3.5))
        plt.title(post)
        colors = plt.cm.viridis([i / len(names) for i in range(len(names))])
        bars = plt.bar(names, counts, color = colors)
        plt.grid(axis = 'y', linestyle = '--', alpha = 0.5)
        for bar, count in zip(bars, counts) :
            yval = bar.get_height()
            plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval + max(counts) * 0.015,  # slight vertical offset
                    str(count),
                    ha = 'center', va = 'bottom',
                    fontsize = 8, color = 'black'
            )
        min_y = min(counts)
        plt.ylim(min_y - 20, max(counts) + 40)
        plt.tight_layout()
        plt.show()



    
if __name__=="__main__":
    make_graphs(get_results_from_db())