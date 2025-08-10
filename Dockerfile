FROM node:18


RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

WORKDIR /app

COPY . .

WORKDIR /app/election-runner
RUN npm install \
    && npx tsc \
    && python3 -m venv venv \
    && ./venv/bin/pip install -r requirements.txt

WORKDIR /app/user-registerer/ur-backend
RUN npm install && npx tsc

WORKDIR /app/user-registerer/ur-frontend 
RUN npm install && npx vite build 

WORKDIR /app
RUN rm -rf election-runner/src/ user-registerer/ur-frontend/src user-registerer/ur-backend/src \
    && echo "Cleaned src files"

RUN chmod +x ./server-script.sh

EXPOSE 5000
EXPOSE 3000


CMD ["./server-script.sh"]