#!/usr/bin/env python3
import random

import openai
import tweepy
from keys import keys
from messages import msgs
from tweepy import API

API_KEY = keys["API_KEY"]
API_SECRET_KEY = keys["API_SECRET_KEY"]
ACCESS_TOKEN = keys["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = keys["ACCESS_TOKEN_SECRET"]

openai.api_key = keys["OPENAPI_SECRET_KEY"]

random_msg = random.choice(msgs)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

limit = api.rate_limit_status()

remaining = limit["resources"]["statuses"]["tweets"]["remaining"]

# Check if API limit has been reached
if remaining == 0:
    print("API rate limit reached. Try again later.")
else:
    try:
        # Find a tweet with certain hashtags to retweet
        tweet = api.search_tweets(
            "#sharklover OR #savesharks OR #sharkdiving OR #ilovesharks OR #protectsharks OR #saveoursharks OR #sharkawareness"
        )[0]

        # Use OpenAI to generate a quote for the tweet
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Retweeting: " + tweet.text,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        comment = response["choices"][0]["text"].strip()

        truncated_text = tweet.text[:277] + "..."
        try:
            api.update_status(truncated_text)
            print("Retweet successful.")
        except tweepy.TweepError as error:
            print("Error. Retweet not successful. Reason:")
            print(error)

        api.update_status(
            "@" + tweet.user.screen_name + " " + comment, in_reply_to_status_id=tweet.id
        )

    except Exception as error:
        print("\nError. Retweet not successful. Reason: ")
        print("Error: " + str(error))
