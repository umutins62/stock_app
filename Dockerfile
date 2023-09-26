# docker için python image kur
FROM python:3.10-slim

RUN apt-get update

RUN apt-get install libpq-dev -y
RUN apt-get install -y python3-dev build-essential
RUN apt-get install  postgresql-client -y

ENV PYTHONDONWRITEBYTECODE 1
ENV VIRTUAL_ENV=/opt/venv

RUN pip install --upgrade pip

RUN pip install virtualenv && python -m virtualenv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ADD ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /srv/app

WORKDIR /srv/app






