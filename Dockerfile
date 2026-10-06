FROM python:3.9-slim-bookworm

RUN pip install pipenv
RUN useradd _gunicorn --no-create-home --user-group

# gunicorn comes from the Pipfile, not apt.
RUN apt-get update && \
    apt-get install -y -q \
        gcc libssl-dev \
        curl postgresql-client git-core

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pipenv install

RUN set -xe \
  && apt-get remove -y gcc python3-dev libssl-dev \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app
