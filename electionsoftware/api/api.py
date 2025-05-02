from fastapi import FastAPI, Request # main fastapi class
from fastapi.responses import HTMLResponse # class to return html as response
from fastapi.staticfiles import StaticFiles #serving static files along with html
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import  CORSMiddleware

from utils import candidate_data

#allowed origins
origins = [
    "http://127.0.0:8000"
]


app = FastAPI()
app.add_middleware(
        CORSMiddleware, # false flag
        allow_origins = "*",
        allow_credentials = True,
        allow_methods = "*",
        allow_headers = "*",
)

app.mount("../static", StaticFiles(directory = "static"))
@app.get("/candidates")
async def get_candidate_data() :
    return candidate_data

@app.get('/voteapp')
async def get_vote_html():
    with open('../templates/main.html', mode= "r") as file:
        return HTMLResponse(content=file.read())

@app.post("/submitvotes")
async def post_votes(request : Request):
    form_data = await request.form()
    votes = dict(form_data)
    print(votes)
    return {
        "status":"success",
        "votes":votes
    }
