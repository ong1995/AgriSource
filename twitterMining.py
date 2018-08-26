import sys
import tweepy
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MineCrop.settings')
django.setup()
from MineCrop_app.models import *

consumer_key = 'yC3XtpO07Ur1EEB4JDYvgQ47n'
consumer_secret = 'd1xmYP7ibcWnsJBFMumFN4Ttxh49Q4ZTLmOGxJuP5oPAKjFhWp'
access_key = '1326659132-uXcpKUlJlEt6VE0TMhOG6qu88kftnveWH2ZzCwf'
access_secret = 'IaYwvUrAC9IPr6VbID4xvNdOWOgzgfBGRy3TiiCQ7Uj2T'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        accepted = False;
        if status.coordinates is not None:
            # check if there is first person keywords found
            # tweet = status.text
            # symptoms_result = find_dengue_symptoms_keywords(tweet)
            # firstPerson_result = find_firstperson_hashtag_keywords(tweet)
            user_id = status.id
            location = status.place.full_name
            date = status.created_at
            long = status.coordinates['coordinates'][0]
            lat = status.coordinates['coordinates'][1]
            name = status.user.name
            c = Coordinate.objects.get_or_create(lng = long, lat = lat)[0]
            c.save()
            t = Tweet.objects.get_or_create(coordinates = c, userid = user_id, name = name, tweet = tweet,
                                            location = location, date = date)[0]
            t.save()
            accepted = True
            print(status.coordinates)

        if accepted == False:
            t = MinedTweet.objects.get_or_create(userid=status.id, username=status.user.name, tweet=status.text, date=status.created_at)[0]
            t.save()

        print(status.text)
        print(status.user.screen_name)

    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(locations=[125.37,7.17,125.45,7.26])
