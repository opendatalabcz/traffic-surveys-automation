FROM tensorflow/tensorflow:2.7.0-gpu

WORKDIR /app

ENV PYTHONPATH /app

RUN apt-get update &&\
    apt-get install -y python3-opencv

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY cli/ ./cli

COPY tsa/ ./tsa
