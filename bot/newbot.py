#!/usr/bin/env python3
import os
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
        except Exception as error:
            print("Error: " + str(error))


#############
# truncated_text = tweet.text[:277] + "..."
# try:
#     api.update_status(truncated_text)
#     print("Retweet successful.")
# except tweepy.TweepError as error:
#     print("Error. Retweet not successful. Reason:")
#     print(error)


# def reply_to_mentions():
#     """Replies to any mentions using chatGPT"""
#     # Get the latest mention
#     mentions = api.mentions_timeline()
#     mention = mentions[0]

#     # Generate the response from OpenAI
#     try:
#         response = (
#             openai.Completion.create(
#                 engine="text-davinci-002",
#                 prompt="@" + mention.user.screen_name + " " + mention.text,
#                 max_tokens=280,
#                 n=1,
#                 stop=None,
#                 temperature=0.5,
#             )
#             .get("choices")[0]
#             .get("text")
#     )

#     if len(response) > 280:
#         response = response[:200] + "..."
#     print("Replied to: " + mention.user.screen_name)

#     # Reply to the mention
#     api.update_status(
#         status="@" + mention.user.screen_name + " " + response,
#         # in_reply_to_status_id=mention.id,
#         auto_populate_reply_metadata=True,
#         exclude_reply_user_ids=None,
#         attachment_url=None,
#         media_ids=None,
#         possibly_sensitive=False,
#         lat=None,
#         long=None,
#         place_id=None,
#         display_coordinates=False,
#         trim_user=False,
#         # verify_status_length=True,
#         # truncate=True,
#     )
# except Exception as error:
#     print("Error: " + str(error))


# def generate_reply():
#     text = mention.text
#     response = (
#         openai.Completion.create(
#             engine="text-davinci-002",
#             prompt=text,
#             max_tokens=200,
#             n=1,
#             stop=None,
#             temperature=0.5,
#         )
#         .get("choices")[0]
#         .text
#     )

#     # return response

#     mentions = api.mentions_timeline()
#     if len(response) > 280:
#         response = response[:200] + "..."
#     print("Replied to: " + mention.user.screen_name)

#     # Reply to each mention
#     try:
#         for mention in mentions:
#             # Get the text of the reply
#             reply_text = generate_reply(mention)

#             # Reply to the mention
#             api.update_status(
#                 status=f"@{mention.user.screen_name} {reply_text}",
#                 in_reply_to_status_id=mention.id,
#             )
#         print("Replied to: " + mention.user.screen_name)
#     except Exception as error:
#         print("Error: " + str(error))


def reply_to_mentions():
    # Get the latest mention
    mentions = api.mentions_timeline()
    latest_mention = mentions[0]

    # Use OpenAI to generate a reply to the latest mention
    model_engine = "text-davinci-002"
    # prompt = "Reply to @" + latest_mention.user.screen_name + ": " + latest_mention.text
    prompt = "Mention a shark fact"

    # Load the ids of replied tweets from a file
    replied_tweet_ids = set()
    if os.path.exists("ids.txt"):
        with open("replied_tweet_ids.txt", "r") as f:
            for line in f:
                replied_tweet_ids.add(int(line.strip()))

    if latest_mention.id not in replied_tweet_ids:
        try:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=160,
                n=1,
                stop=None,
                temperature=0.5,
            )
            reply = completion.choices[0].text
            reply = f"Thanks @{latest_mention.user.screen_name}, let me throw a shark fact at ya: {reply}"

            # Post the reply
            api.update_status(status=reply, in_reply_to_status_id=latest_mention.id)
            print("Successfully replied with:", reply)
            # Add the tweet id to the set of replied tweet ids
            replied_tweet_ids.add(latest_mention.id)
        except Exception as e:
            print("Error:", e)


reply_to_mentions()
# generate_reply()
# reply_to_mentions()
# retweet_comment_and_like()
