from keras import models
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
import numpy as np
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

def twitter_processor(tweets):
    model = models.load_model(os.path.join(BASE, "model/model1.h5"))
    response = []
    for tweet in tweets:
        x = [tweet['tweet']]
        tokenizer = Tokenizer(num_words=None, split=' ')
        tokenizer.fit_on_texts(x)
        x = tokenizer.texts_to_sequences(x)
        x = pad_sequences(x, maxlen=20, padding='post')

        prediction = model.predict(x)    
        print("pred:::::", prediction, "tweet::::::::::::::", tweet, "\n")
        tweet_info = {
            'Harazment' : 0,
            'Sexual' : 0,
            'Mental' : 0,
            'Indirect' : 0
        }
        pred_response = {
            "status": 0,
            "nature": ''
        }
        if prediction[0,0]>=0.4:
            tweet_info['Harazment'] = 1
            pred_response['status'] = 1
            t=np.argmax(prediction[0,1:])
            if t==2:
                tweet_info['Sexual'] = 1
                pred_response['nature'] = 'Sexual'
            elif t==1:
                tweet_info['Mental'] = 1
                pred_response['nature'] = 'Mental'
            elif t==0:
                tweet_info['Indirect'] = 1
                pred_response['nature'] = 'Indirect'
        #tweet_info.update(tweet)
        pred_response.update(tweet)
        response.append(pred_response)
    return response