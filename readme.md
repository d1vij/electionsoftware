# Voting Application

A lightweight, asynchronous voting application with a MongoDB backend. It consists of two independent servers:  
- **User Registerer** (for setting up posts and candidates)  
- **Election Runner** (for conducting the vote and showing results)  

Built using FastAPI and Express.js, and containerized using Docker for easy deployment.
---

> [!NOTE]
> Prebuilt image _`docker pull d1vij/es-image:080725`_ (just edit .env)

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/d1vij/electionsoftware
cd electionsoftware
````

### 2. Configure MongoDB

Create a cluster on [MongoDB Atlas](https://cloud.mongodb.com) (or host locally).
Then, set up your `.env` file with the correct credentials:

```ini
CONNECTIONSTRING="mongodb+srv://<user>:<password>@cluster.mongodb.net/"
DATABASE_NAME="voting"
ACTIVE_COLLECTION="votes"
PASSWORD="1234"

# Server Mode
# RUN = 0 -> Run Election Server (port 3000)
# RUN = 1 -> Run User Registerer Server (port 3000)
# RUN = 2 -> Run both (Election on 5000, Registerer on 3000)
```

### 3. Build Docker Image

Make sure Docker is installed. Then run:

```sh
docker build -t es-image .
```

### 4. Run the Container

```sh
docker run --name es-container es-image
```

> After the image is built, `.env` can be updated from inside the container at `/app/.env`.

---

## Configuration
### Setting up Candidates and Posts

1. Run the `user-registerer` server.
2. Open `http://localhost:3000/index.html` in your browser.
3. Use the form to configure posts and candidates.

> **Note:** Once submitted, candidate data **cannot** be modified through the form. To manually edit, go to `/election-runner/static/candidate-data/candidates.json` and make changes there

```json
// election-runner/static/candidate-data/candidates.json
[
  {
    "name": "Head boy",
    "candidates": [
      {
        "name": "Divij",
        "candidateId": "f46a663f-bff4-4083-a2c6-91ba9960402f"
      },
      ...
    ]
  },
  ...
]
```

### Candidate Images

Candidate images must be stored in `/images/`, with filenames matching their `candidateId`:

```
images/
└── cd0e2a07-cfdd-4c5b-b2b9-bc95b22ecf5e.png
```

---

## Starting the Server

The appropriate server(s) start automatically when the Docker container is run, based on the value of `RUN` in `.env`.

---

## Endpoints

### User Registerer (`RUN = 1` or `2`)

* `/register` → Candidate/Post creation form

### Election App (`RUN = 0` or `2`)

* `/voteapp` → Voting interface
* `/results` → Displays results

---

## Database Structure

Votes are stored as documents in the `votes` collection:

```json
{
  "_id": "...",
  "token": "fcc68311ebb8c02e57c2eddf7a0a596eb98c6c73e56cb3a5c34ca079543ef221",
  "vote_data": [
    {
      "name": "Divij",
      "post": "head_boy"
    },
    {
      "name": "Shruti",
      "post": "head_girl"
    }
  ]
}
```

> **Security Note:**
> The voting page is rendered with hidden HTML elements toggled by CSS. Although the vote form is hidden until login, a  user can manipulate the HTML to make it visible. While the submit button remains disabled until proper login, this still introduces a potential attack surface. This should be secured in future versions.

---

## Tech Stack

### Frontend

* TypeScript
* HTML & CSS

### Backend

* **User Registerer**:

  * Node.js + Express
  * Multer (for file handling)

* **Election Runner**:

  * FastAPI
  * Uvicorn (ASGI Server)
  * Motor (async MongoDB client)
  * Matplotlib (for result visualization)

---

## Application Views

### Voting App Interface

![Voting App](voteapp.png)

### Result Display

![Results](results.png)

