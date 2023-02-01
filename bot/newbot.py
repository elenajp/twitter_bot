import keys
import openai
import tweepy

# Twitter API credentials
consumer_key = "CONSUMER_KEY"
consumer_secret = "CONSUMER_SECRET"
access_token = "ACCESS_TOKEN"
access_token_secret = "ACCESS_TOKEN_SECRET"

# Authenticate API client
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# OpenAI API key
openai.api_key = "OPENAPI_SECRET_KEY"

def reply_to_mentions():
    mentions = api.mentions_timeline()
    for mention in mentions:
        if mention.in_reply_to_status_id is None:
            message = mention.text
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"{message}\n",
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text
            api.update_status(
                status=f"@{mention.user.screen_name} {response}"
                in_reply_to_status_id=mention.id,
            )