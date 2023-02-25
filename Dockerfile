FROM python:3.10.0a7-buster

WORKDIR /twitter_bot

COPY requirements.txt /twitter_bot
RUN pip3 install -r requirements.txt

COPY /twitter_bot .

CMD [ "python3", "twitterbot.py" ]