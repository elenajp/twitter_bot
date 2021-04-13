#!/usr/bin/env python3
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


# mentions = api.mentions_timeline()
# for mention in mentions:
#     print(mention.id)

last_Seen_id = retrieve_id(FILE)
mentions = api.mentions_timeline(last_Seen_id, tweet_mode='extended')
for mention in reversed(mentions):
    if 'shark' in mention.full_text:
        last_Seen_id = mention.id
        store_id(last_Seen_id, FILE)
        api.update_status('@'+mention.user.screen_name + 'YAY', mention.id)
        print('Replied to @' + mention.user.screen_name)


key_words = ['#shark', '#sharks', '#sharkweek', 'sharks', 'shark']
msgs = [
    'Being left-handed kills more people than sharks! 2, 500 people die each year after using right-handed items incorrectly. Sorry, lefties.',
    'Armed toddlers kill more people than sharks! 21 people die each year from toddlers wielding a gun they found in an unlocked cabinet.',
    'Elephants kill more people than sharks! Those cute, cuddly animals that everyone adores? Yeah, they kill 600 people a year. Tough love.'
]
