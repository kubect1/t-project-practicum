FROM python:3.12.3

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

WORKDIR /trips-reminder


COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install


COPY app ./app
COPY celery_queue ./celery_queue

