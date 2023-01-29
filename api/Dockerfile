FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN mkdir /code

WORKDIR /code

ADD ./pyproject.toml /code/

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install --upgrade poetry

RUN poetry install