#!/bin/bash

echo "-> Setup RUN variable in .env"
source .env

if [ "$RUN" = "0" ]; then
    echo "Starting election-runner on port 3000"
    ./election-runner/venv/bin/uvicorn election-runner.api.main:app --host 0.0.0.0 --port 3000 &

elif [ "$RUN" = "1" ]; then
    echo "Starting user-registerer on port 3000"
    node user-registerer/ur-backend/dist/server.js &

elif [ "$RUN" = "2" ]; then
    echo "Starting election-runner on port 5000 and user-registerer on port 3000"
    echo "*** THIS WILL ONLY WORK LOCALLY ***"

    ./election-runner/venv/bin/uvicorn election-runner.api.main:app --host 0.0.0.0 --port 5000 &
    node user-registerer/ur-backend/dist/server.js &

else
    echo "Invalid RUN value: $RUN"
    echo "Expected 0, 1, or 2."
    exit 1
fi

wait
