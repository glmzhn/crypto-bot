FROM python:3.12-alpine3.19

COPY requirements.txt /temp/requirements.txt
WORKDIR crypto-bot
ADD . /crypto-bot

RUN pip install -r /temp/requirements.txt