# About
A lightweight voting application with MongoDB backend and FastAPI-based server. Uses Asynchronous paradigm to allow for concurrent voting sessions. 

## Installation steps
* Clone this repo into a directory and cd into it
```ps
$ git clone https://github.com/d1vij/electionsoftware/
$ cd electionsoftware
```

* Make python venv and install dependencies
```ps
$ py -m venv .venv
$ .venv/scripts/activate
$ pip install -r requirements.txt
```
* Create a cluster on [MongoDB atlas](https://cloud.mongodb.com) or host locally. In api/utils.py change connection parameters
```py
# if using connection string
CONNECTIONSTRING = "mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@server.example.com/"

#if using local database
URL="http://127.0.0.1"
PORT=1234
```
## Other setup
* Setting up candidate data by going into `./api/utils.py`. Candidate data is a python dictionary with keys as post names and array of candidate names as its value.
> Note that post names must be of valid json type and without spaces. Post names with underscores are automatically formatted when during voting
```py
#eg
candidate_data = {
    "head_boy": ["Divij", "Rohan", "Aditya", "Karan", "Nishant"],
    "head_girl": ["Aisha", "Shruti", "Meera", "Anita", "Priya"],
    "sports_captain": ["Rahul", "Arjun", "Vivek", "Kavya", "Tarun"]
}
```

* Candidate image's name **must** be exactly similar to that particular candidates' name. Candidates with underscores in their names would be normalized to have spaces instead, but **dont** keep spaces by default in candidate names. 
  Images to be stored in `/public/img/` and all with common extension. The default extension is png but it could be configured in the `main.js` file.


* Custom password can be set by storing a hexdigested string of sha256 hash of your password in `PASSWORD_HASH` of `/public/script.js` (default password is `1234`)
  



## Starting server
* To start server from root directory
```ps
$ uvicorn api.main:app --port 9000
```
> This starts server on current device's ip (like localhost:9000/)

## Miscell utilities
~ by directly running `/api/utils.py`

`fakedata` -> generate dummy votes and auto post them to database
`PLEASEDELETEVOTES` -> delete all the votes from database

## Endpoints
* Client wise important endpoints include
    * `/voteapp` -> The main application
    * `/results` -> Viewing results
* Documentation of all other endpoints could be found at `/docs` endpoint

> The `/` endpoint is not configured to return/redirect anything, by going to `/gettoken` we can check if server is runnning correctly


## Database
* Each vote is saved as an document inside of database `DATABASE` and collection `ACTIVE_COLLECTION` , both of which are present in `./api/utils.py`
* Vote document is in the below format, and can easily be compiled through a simple script (or by using /results endpoint )
```json
{
  "_id": ...,
  "token": "fcc68311ebb8c02e57c2eddf7a0a596eb98c6c73e56cb3a5c34ca079543ef221",
  "vote_data": [
    {
      "name": "Divij",
      "post": "head_boy"
    },
    {
      "name": "Shruti",
      "post": "head_girl"
    },
    ...
  ]
}
```

> [!IMPORTANT]
> Currently how the vote app is rendered is that when client recieves the static html file, all form buttons are generated dynamically and are hidden with a css class (name  _hidden_). When successful login is done, hidden class is toggled between login div and vote-form div. This means that user could simple go and edit the respective classes in html and make the vote form visible. Although the submit button is disabled, this should be kept in mind how easily exploitable is current system :).


<hr>
<br>

![](voteapp.png)
![](results.png)

<hr>

## Tech stack used
* Frontend
  * Typescript
  * Html (+css)

* Backend
  * FastAPI - main backend api server
  * Uvicron - ASGI
  * Motor - asynchronous mongodb connector
  * Matplotlib - generating graphs
  
  
<hr>
