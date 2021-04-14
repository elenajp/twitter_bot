#!/usr/bin/env python3
import random
import time

import tweepy

from keys import keys
from messages import msgs

API_KEY = keys['API_KEY']
API_SECRET_KEY = keys['API_SECRET_KEY']
ACCESS_TOKEN = keys['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = keys['ACCESS_TOKEN_SECRET']

keywords = ['#sharklover', '#savesharks',
            '#sharkweek', '#sharkdiving', '#ilovesharks']
random_keyword = random.choice(keywords)
# keywords = ['#atesthash']


random_msg = random.choice(msgs)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

FILE = 'id.txt'


def retrieve_id(file):
    f_read = open(file, 'r')
    last_seen_id = int(f_read.read().strip())  # grabs the id in the file
    f_read.close()
    return last_seen_id


def store_id(id, file):
    f_write = open(file, 'w')
    f_write.write(str(id))
    f_write.close()
    return


last_Seen_id = retrieve_id(FILE)
mentions = api.mentions_timeline(last_Seen_id, tweet_mode='extended')

for mention in reversed(mentions):
    try:
        for i in keywords:
            if i in mention.full_text:
                last_Seen_id = mention.id
                store_id(last_Seen_id, FILE)
                api.update_status('@'+mention.user.screen_name +
                                  f' {random_msg}', mention.id)
                print('Replied to @' + mention.user.screen_name)

    except tweepy.TweepError as error:
        print('\nError. Retweet not successful. Reason: ')
        print(error.reason)


for tweet in tweepy.Cursor(api.search, q=random_keyword, lang="en").items(5):
    try:
        print('\nRetweet Bot found tweet by @' +
              tweet.user.screen_name + '. ' + 'Attempting to retweet.')

        tweet.retweet()
        print('Retweet published successfully.')

        time.sleep(60)

    except tweepy.TweepError as error:
        print('\nError. Retweet not successful. Reason: ')
        print(error.reason)

    except StopIteration:
        break
