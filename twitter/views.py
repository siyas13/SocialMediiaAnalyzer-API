
from django.shortcuts import render
from rest_framework.views import APIView
from twython import Twython
import json
import pandas as pd
from rest_framework.response import Response
from .utils import twitter_processor
import tweepy

class TwitterAPI(APIView):

    def get(self, request):
        with open("twitter_credentials.json", "r") as file:
            creds = json.load(file)

        python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

        key = request.GET.get("keyword", None)
        if key:
            query = {'q': key,
            'count': 4,
            'lang': 'en',
            }
            dict_ = {'user': [], 'user_id': [], 'date': [], 'tweet': [], 'favorite_count': []}

            for status in python_tweets.search(**query)['statuses']:
                print(".....................", status)
                dict_['user'].append(status['user']['screen_name'])
                dict_['user_id'].append(status['user']['id'])
                dict_['date'].append(status['created_at'])
                dict_['tweet'].append(status['text'])
                dict_['favorite_count'].append(status['favorite_count'])
            df = pd.DataFrame(dict_)
            data = [{"name": dict_["user"][i], "tweet": dict_["tweet"][i], "user_id": dict_["user_id"][i], "date": dict_["date"][i]} for i in range(0, len(dict_["user"]))]
            # df.sort_values(by='favorite_count', inplace=True, ascending=False)
            return Response(data)

class Analyzer(APIView):
    def post(self, request):
        #data = [{"name": request.data["data"]["user"][i], "tweet": request.data["data"]["text"][i]} for i in range(0, len(request.data["data"]["user"]))]
        response = twitter_processor(request.data)
        return Response(response)

class ReportAndBlock(APIView):
    def post(self, request):
        user_data = request.data
        with open("twitter_credentials.json", "r") as file:
            creds = json.load(file)
        twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        oauth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        oauth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
        api = tweepy.API(oauth)
        name = user_data['name']
        print("::::::::::", user_data)
        print(".............", name)
        api.create_block(screen_name = name)

        return Response(user_data)
