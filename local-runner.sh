#!/usr/bin/bash
read  -p "Which server to run ?
[E | 0] Election-runner
[U | 1] User-registerer
[B | 2] Both (default)
->" choice

if [ "$choice" == "0" ] || [ "$choice" == "E" ];
then 
    echo "Running Election-runner on port 3000
    Access site on /voteapp"
    ./election-runner/venv/bin/uvicorn election-runner.api.main:app --host 0.0.0.0 --port 3000 &

elif [ "$choice" == "1" ] || [ "$choice" == "U" ];
then
    echo "Running User Registerer on port 3000
    Access site on /index.html"
    node user-registerer/ur-backend/dist/server.js &
else
    echo "Running User Registerer on port 3000
    and election runner on port 5000"

    ./election-runner/venv/bin/uvicorn election-runner.api.main:app --host 0.0.0.0 --port 5000 &
    node user-registerer/ur-backend/dist/server.js &
fi

wait
