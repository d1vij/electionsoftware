#!/bin/bash
./election-runner/venv/bin/uvicorn election-runner.api.main:app --host 0.0.0.0 --port 5000 &
node user-registerer/ur-backend/dist/server.js &
wait
