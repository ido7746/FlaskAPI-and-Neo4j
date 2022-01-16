FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . /app

RUN pip install -r requirements.txt

CMD [ "python", "app.py"]