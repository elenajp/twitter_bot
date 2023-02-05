#!/usr/bin/env python3
import random

import openai
import tweepy
from keys import keys
from tweepy import Cursor

API_KEY = keys["API_KEY"]
API_SECRET_KEY = keys["API_SECRET_KEY"]
ACCESS_TOKEN = keys["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = keys["ACCESS_TOKEN_SECRET"]

openai.api_key = keys["OPENAPI_SECRET_KEY"]

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def retweet_comment_and_like():
    """Retweets Twitter posts containing a specific hashtag, likes the tweet and comments on it too"""
    hashtags = "#saveoursharks OR #sharkawareness OR #sharklover OR #savesharks OR #sharkdiving OR #ilovesharks OR #protectsharks"
    for tweet in Cursor(
        api.search_tweets, q=hashtags, lang="en", tweet_mode="extended"
    ).items(2):
        try:
            if not tweet.retweeted:
                api.retweet(tweet.id)
                tweet.favorite()
                status = api.get_status(tweet.id, tweet_mode="extended")
                screen_name = status.user.screen_name
                message = f"@{screen_name} Great tweet! I really enjoyed it."
                api.update_status(message, in_reply_to_status_id=tweet.id)
                print("Retweeted tweet: " + tweet.full_text)
            # except tweepy.errors.TweepyException as error:
        except Exception as error:
            print("Error: " + str(error))


retweet_comment_and_like()
