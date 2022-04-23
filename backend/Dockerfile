FROM tensorflow/tensorflow:2.7.0-gpu

WORKDIR /app

ENV PYTHONPATH /app

RUN apt-get update &&\
    apt-get install -y python3-opencv &&\
    pip install poetry &&\
    poetry config virtualenvs.create false

COPY alembic.ini poetry.lock pyproject.toml ./

RUN poetry install --no-dev

COPY migrations/ ./migrations

COPY cli/ ./cli

COPY tsa/ ./tsa

CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "80", "tsa.app.app:fast_app"]

EXPOSE 80
