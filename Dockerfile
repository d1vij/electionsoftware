FROM python:3.13
WORKDIR /electionsoftware-image

COPY ./requirements.txt /electionsoftware-image/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /electionsoftware-image/requirements.txt

COPY . /electionsoftware-image/

EXPOSE 8000
CMD [ "uvicorn","api.main:app","--host","0.0.0.0","--port","8000" ]
