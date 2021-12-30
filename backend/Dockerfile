FROM tensorflow/tensorflow:2.7.0-gpu

WORKDIR /app

ENV PYTHONPATH /app

RUN apt-get update &&\
    apt-get install -y python3-opencv &&\
    pip install poetry &&\
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

COPY cli/ ./cli

COPY tsa/ ./tsa
