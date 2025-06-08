
import matplotlib.pyplot as plt
from io import BytesIO
from base64 import b64encode
import asyncio
from pprint import pprint
from .models import VoteResponse
from .database_wrapper import DatabaseWrapper

from .utils import CONNECTIONSTRING, DATABASE_NAME, ACTIVE_COLLECTION,candidate_data
from .utils import Log


async def makeGraph(post, vote_dict) -> str:
    # Sort by vote count (descending)
    sorted_items = sorted(vote_dict.items(), key=lambda x: x[1], reverse=True)
    names, counts = zip(*sorted_items)
    plt.figure(figsize=(6, 3.5))
    plt.title(post)
    colors = plt.cm.viridis([i / len(names) for i in range(len(names))]) # type: ignore
    bars = plt.bar(names, counts, color=colors)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    for bar, count in zip(bars, counts):
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + max(counts) * 0.015,  # slight vertical offset
            str(count),
            ha='center', va='bottom',
            fontsize=8, color='black'
        )
    min_y = min(counts)
    plt.ylim(min_y - 20, max(counts) + 40)
    plt.tight_layout()

    buffer = BytesIO()

    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # plt.close() # this here causes
    return f"data:image/png;base64,{b64encode(buffer.read()).decode('utf-8')}"





async def getResultGraphs() -> list[str]:
    """
    generates result graphs for each post and returns array of dataurls corresponding to each graph
    """
    connObj = DatabaseWrapper(
        connection_string=CONNECTIONSTRING,
        database=DATABASE_NAME
    )

    all_documents: list[VoteResponse] = await connObj.fetchResults(collection=ACTIVE_COLLECTION)
    compiled_results = {p: dict.fromkeys(candidate_data[p], 0) for p in candidate_data.keys()}

    print("Empty results dict")
    pprint(compiled_results,indent=2)

    Log.info(f"Total documents found {len(all_documents)}")

    seen_tokens = []
    document: VoteResponse
    # updating votes from results
    for document in all_documents:
        try:
            token = document['token']              # type: ignore
            if not (token in seen_tokens):
                seen_tokens.append(token)
                for vote in document['vote_data']: # type: ignore
                    try:
                        post_name = vote["post"]
                        voted_candidate = vote['name']
                        curPostCandidates = compiled_results[post_name]
                        curPostCandidates[voted_candidate] += 1
                    except Exception as e:
                        Log.warning(str(e))
        except Exception as e:
            print(document)
            exit()
    img_data = await asyncio.gather(*[makeGraph(post, vote_dict) for post, vote_dict in compiled_results.items()])

    pprint(compiled_results)
    return img_data
