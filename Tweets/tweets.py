#written by Maximilian Langewort

import json
import pymongo
import tweepy
import gc
#your Keys
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''
# s_lng = 60.2
# s_lat = 24.8
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    # Starts at intialization of the class
    def __init__(self, api):
        #Transfer of the API
        self.api = api
        #Start stream
        super(tweepy.StreamListener, self).__init__()
        #Opens your local MongoDB-Connection
        self.db = pymongo.MongoClient().Twitter

    # During the stream
    def on_data(self, tweet):
        #transforms the received data into JSON
        data = json.loads(tweet)
        #if the Tweet has a message...
        if 'text' in data:

            #if 'pub' in data['text'].lower() or 'ravintola' in data['text'].lower() or 'kapakka' in data['text'].lower() or 'yökerho'in data['text'].lower():
                self.db.Pubs_search.insert(data)
                print('success')

            #else:
                #manually start the Garbage-Collector
                #search for an expression and filter the area of the coordinates to prevent insertion of existing tweets. Just for non-stream-querys.
                gc.collect()
        #if 'coordinates' in data:
        #    if data['coordinates'] is not None:
        #        self.db.Pubs.insert(json.loads(tweet))
        #        a=data['coordinates']['coordinates'][1]
        #        if (a>(s_lng-0.5)):
        #            if(data['coordinates']['coordinates'][1] < s_lng+0.5):
        #                if (data['coordinates']['coordinates'][2] > s_lat - 0.5):
        #                    if(data['coordinates']['coordinates'][2] > s_lat + 0.5):
        #                        self.db.Pubs_search.insert(json.loads(tweet))
        #                        print(tweet)
        #        else:
        #            gc.collect()
    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream


def Twitter_search(lat, lng):
    #get a stream
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
    #sapi.filter(track=['Pub', 'ravintola', 'kapakka', 'yökerho'])
    #set a filter for the stream
    sapi.filter(locations=[lat-0.5,lng-0.5,lat+0.5,lng+0.5])
