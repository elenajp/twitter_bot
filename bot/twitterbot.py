#!/usr/bin/env python3
import random
import time
from urllib.parse import urlencode

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

FILE = "id.txt"


def retrieve_id(file):
    f_read = open(file, "r")
    last_seen_id = int(f_read.read().strip())  # grabs the id in the file
    f_read.close()
    return last_seen_id


def store_id(id, file):
    f_write = open(file, "w")
    f_write.write(str(id))
    f_write.close()
    return


# last_Seen_id = retrieve_id(FILE)
# mentions = api.mentions_timeline(last_Seen_id, tweet_mode="extended")

# for mention in reversed(mentions):
#     try:
#         if "#savesharks" in mention.full_text:
#             last_Seen_id = mention.id
#             store_id(last_Seen_id, FILE)
#             api.update_status(
#                 "@" + mention.user.screen_name + f" {random_msg}", mention.id
#             )
#             print("Replied to @" + mention.user.screen_name)

#     except tweepy.TweepError as error:
#         print("\nError. Retweet not successful. Reason: ")
#         print(error.reason)

############################################################################################
# the code below is the original and working
# for word in keywords:
#     for tweet in tweepy.Cursor(api.search_tweets, q=word, lang="en").items(5):
#         try:
#             print(
#                 "\nRetweet Bot found tweet by @"
#                 + tweet.user.screen_name
#                 + ". "
#                 + "Attempting to retweet."
#             )

#             tweet.retweet()
#             print("Retweet published successfully.")

#             tweet.favorite()
#             print("Favorited the tweet")

#             time.sleep(60)

#         except Exception as error:
#             print("\nError. Retweet not successful. Reason: ")
#             print("Error: " + str(error))

############################################################################################


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

    # if len(tweet.text) > 280:
    #     tweet_text = tweet.text[:277] + "..."
    # else:
    #     tweet_text = tweet.text
    truncated_text = tweet.text[:277] + "..."
    try:
        api.update_status(truncated_text)
        print("Retweet successful.")
    except tweepy.TweepError as error:
        print("Error. Retweet not successful. Reason:")
        print(error)

    # Quote the tweet and retweet it
    # api.update_status("Retweeting: " + tweet.text + "\n\nQuote: " + quote, tweet.id)
    # api.update_status(
    #     "Retweeting: " + tweet.text + "\n\nQuote: " + comment,
    #     in_reply_to_status_id=tweet.id,
    # )
    api.update_status(
        "@" + tweet.user.screen_name + " " + comment, in_reply_to_status_id=tweet.id
    )
# except tweepy.TweepyError as error:
#     print("Error: " + str(error.reason))
# except Exception as error:
#     print("Error: " + str(error))

except Exception as error:
    print("\nError. Retweet not successful. Reason: ")
    print("Error: " + str(error))
