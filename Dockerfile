# Feel free to change base image
FROM python:3.9.7-slim-buster

WORKDIR /src

RUN apt-get update && \
    apt-get install --assume-yes --no-install-recommends \
    # Needed to build python packages
    gcc \
    libc-dev \
    # Needed for psycopg
    libpq-dev && \
    rm --recursive --force /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --progress-bar=off poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction

COPY . .
