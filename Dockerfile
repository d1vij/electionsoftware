FROM node:18

# Install Python and venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Create work directory
WORKDIR /app

# Copy everything
COPY . .

# ======= Setup FastAPI backend =======
WORKDIR /app/election-runner
RUN npm install
RUN npx tsc
RUN python3 -m venv venv
RUN ./venv/bin/pip install --upgrade pip \
    && ./venv/bin/pip install  -r requirements.txt

# ======= Setup Express backend =======
WORKDIR /app/user-registerer/ur-backend
RUN npm install
RUN npx tsc

# ======= Build Frontend =======
WORKDIR /app/user-registerer/ur-frontend
RUN npm install
RUN npx vite build

# ======= Startup Script =======
WORKDIR /app
RUN chmod +x ./server-script.sh

EXPOSE 5000
EXPOSE 3000

CMD ["./server-script.sh"]
# CMD ["python3","./server-script.py"]
