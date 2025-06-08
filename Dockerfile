FROM node:18

# This file goes and builds application components one by one

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

WORKDIR /app

COPY . .

WORKDIR /app/election-runner
RUN npm install
RUN npx tsc
RUN python3 -m venv venv
RUN ./venv/bin/pip install --upgrade pip \
    && ./venv/bin/pip install  -r requirements.txt

WORKDIR /app/user-registerer/ur-backend
RUN npm install
RUN npx tsc

WORKDIR /app/user-registerer/ur-frontend
RUN npm install
RUN npx vite build

WORKDIR /app
RUN chmod +x ./server-script.sh

EXPOSE 5000
EXPOSE 3000

CMD ["./server-script.sh"]