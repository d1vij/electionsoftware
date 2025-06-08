#!/bin/bash

# Start FastAPI (assuming main.py has app defined in it)
./election-runner/venv/bin/uvicorn election-runner.api.main:app --host 0.0.0.0 --port 5000 --reload &

# Start Express backend
node user-registerer/ur-backend/dist/server.js &

# Wait to keep container alive
wait
