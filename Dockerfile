FROM python:3.12-alpine3.19

COPY requirements.txt /temp/requirements.txt
WORKDIR /telegram-bot
COPY telegram-bot /telegram-bot

RUN pip install -r /temp/requirements.txt

CMD ["python", "main.py"]