#!/usr/bin/env python3

import os

import tweepy

from keys import keys

API_KEY = keys['api_key']
API_SECRET_KEY = keys['api_secret_key']
BEARER_TOKEN = keys['bearer_token']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

key_words = ['shark', 'sharks', 'shark week', 'sharkweek']
msgs = [
    'Being left-handed kills more people than sharks! 2, 500 people die each year after using right-handed items incorrectly. Sorry, lefties.',
    'Armed toddlers kill more people than sharks! 21 people die each year from toddlers wielding a gun they found in an unlocked cabinet.',
    'Elephants kill more people than sharks! Those cute, cuddly animals that everyone adores? Yeah, they kill 600 people a year. Tough love.'
]
