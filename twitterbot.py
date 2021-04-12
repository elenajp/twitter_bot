#!/usr/bin/env python3

import os

import tweepy

from keys import keys

API_KEY = keys['API_KEY']
API_SECRET_KEY = keys['API_SECRET_KEY']
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# api variable used to execute various methods and interact with twitter
api = tweepy.API(auth)

FILE = 'id.txt'

# retrieve_id grabs id from text file used it, grab last id and save it in text file


def retrieve_id(file):
    f_read = open(file)  # opens the file
    last_seen_id = int(f_read.read().strip())  # grabs the id in the file
    f_read.close()
    print(last_seen_id)  # closes the file
    return last_seen_id


retrieve_id(FILE)


# mentions = api.mentions_timeline()
# for mention in mentions:
#     print(mention.id)

key_words = ['shark', 'sharks', 'shark week', 'sharkweek']
msgs = [
    'Being left-handed kills more people than sharks! 2, 500 people die each year after using right-handed items incorrectly. Sorry, lefties.',
    'Armed toddlers kill more people than sharks! 21 people die each year from toddlers wielding a gun they found in an unlocked cabinet.',
    'Elephants kill more people than sharks! Those cute, cuddly animals that everyone adores? Yeah, they kill 600 people a year. Tough love.'
]
