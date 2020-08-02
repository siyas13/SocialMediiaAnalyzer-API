from keras import models
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.preprocessing import text, sequence
import numpy as np
import pandas as pd
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

def twitter_processor(tweets):
    model = models.load_model(os.path.join(BASE, "model/twitter_harassment_pred.h5"))
    response = []
    train_x = pd.read_csv(os.path.join(BASE, "train_preprocessed.csv")).fillna(" ")
    max_features=100000
    maxlen=150
    embed_size=300
    train_x['comment_text'].fillna(' ')
    train_y = train_x[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']].values
    train_x = train_x['comment_text'].str.lower()
    for tweet in tweets:
        x = [tweet['tweet']]
        tokenizer = text.Tokenizer(num_words=max_features, lower=True)
        tokenizer.fit_on_texts(list(train_x))
        x = tokenizer.texts_to_sequences(x)
        x = pad_sequences(x, maxlen=maxlen)

        prediction = model.predict(x)    
        print("pred:::::", prediction, "tweet::::::::::::::", tweet, "\n")
        tweet_info = {
            'status' : 0,
            'Toxic' : 0.0,
            'SevereToxic' : 0.0,
            'Obscene' : 0.0,
            'Threat' : 0.0,
            'Insult' : 0.0,
            'IdentityHate' : 0.0,
        }
        if prediction[0,0]>=0.4:
            tweet_info['status'] = 1
        tweet_info['Toxic'] = prediction[0,0]*100
        tweet_info['SevereToxic'] = prediction[0,1]*100
        tweet_info['Obscene'] = prediction[0,2]*100
        tweet_info['Threat'] = prediction[0,3]*100
        tweet_info['Insult'] = prediction[0,4]*100
        tweet_info['IdentityHate'] = prediction[0,5]*100
        tweet_info.update(tweet)
        response.append(tweet_info)
    return response