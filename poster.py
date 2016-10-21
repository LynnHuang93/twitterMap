#!/usr/bin/python
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime
from elasticsearch import Elasticsearch
import dateutil.parser
import time
import string
import config
import json

es = Elasticsearch(['https://search-xingling-rt-twitter-map-2sqqiexw5xrhqcxx4x5o6d2a3y.us-west-2.es.amazonaws.com'])

class MyListener(StreamListener):
    """Custom StreamListener for streaming data"""

    def __init__(self, api=None):
        super(MyListener, self).__init__()

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            t = dateutil.parser.parse(tweet['created_at'])

            data_dict = {
                    "username": tweet["user"]["name"],
                    "created_at": t.isoformat("T") + "Z",
                    "text": tweet["text"]
                }
            
            if 'geo' in tweet and tweet["geo"]:
                data_dict['latitude'] = tweet["geo"]["coordinates"][1]
                data_dict['longtitude'] = tweet["geo"]["coordinates"][0]
                res = es.index(index='tweet', doc_type='tweet', id=tweet["id"], body=data_dict)
                print(" response: '%s'" % (res))
            elif 'place' in tweet and tweet["place"] and any(tweet["place"]["bounding_box"]):
                bbox = tweet["place"]["bounding_box"]["coordinates"][0]
                data_dict['latitude'] = 0 if bbox[0][0] + bbox[1][0] + bbox[2][0] + bbox[3][0] == 0 else (bbox[0][0] + bbox[1][0] + bbox[2][0] + bbox[3][0])/4.0
                data_dict['longtitude'] = 0 if bbox[0][1] + bbox[1][1] + bbox[2][1] + bbox[3][1] == 0 else (bbox[0][1] + bbox[1][1] + bbox[2][1] + bbox[3][1])/4.0
                res = es.index(index='tweet', doc_type='tweet', id=tweet["id"], body=data_dict)
                print(" response: '%s'" % (res))

            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    request_body = {
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }

    res = es.indices.create(index = 'tweet', body = request_body, ignore=400)
    print(" response: '%s'" % (res))
    while True:
        try:
            twitter_stream = Stream(auth, MyListener())
            twitter_stream.filter(locations=[-180, -90, 180, 90])
        except BaseException:
            continue
        except KeyboardInterrupt:
            stream.disconnect()
            break
