FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
RUN mkdir /code/staticfiles
WORKDIR /code

ADD . /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk update && apk add bash
