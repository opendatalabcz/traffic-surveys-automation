FROM python:3.9-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

COPY cli/ ./cli

COPY tsa/ ./tsa
