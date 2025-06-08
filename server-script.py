#!/usr/bin/env python3
import subprocess

fastapi_command = [
    "./election-runner/venv/bin/uvicorn",
    "election-runner.api.main:app",
    "--host", "0.0.0.0",
    "--port", "5000",
    "--reload"
]
nodejs_command = [
    "node",
    "user-registerer/ur-backend/dist/server.js"
]

def main():
    
    c = int(input("Which server to run \n (default)Both\n(1)Register user\n(2)Main Election runner\n-->"))
    c=0
    match c:
        case 1:
            try:
                nodejs_cmd = subprocess.Popen(nodejs_command)
                nodejs_cmd.wait()
            except KeyboardInterrupt:
                print("exiting...")
                nodejs_cmd.terminate()
        case 2:
            try:
                fastapi_cmd = subprocess.Popen(fastapi_command)
                fastapi_cmd.wait()
            except KeyboardInterrupt:
                print("exiting...")
                fastapi_cmd.terminate()
        case _:
            try:
                nodejs_cmd = subprocess.Popen(nodejs_command)
                fastapi_cmd = subprocess.Popen(fastapi_command)

                nodejs_cmd.wait()
                fastapi_cmd.wait()
            except KeyboardInterrupt:
                print("exiting...")
                nodejs_cmd.terminate()
                fastapi_cmd.terminate()

            
        

if __name__ == "__main__":
    main()