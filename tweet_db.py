# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 14:47:51 2022

@author: 35387
"""
#%%
import tweepy
import sqlite3 as lite

import pandas as pd
import gensim
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from pprint import pprint
#%%
def collect_tweets(screen_names):
    con = lite.connect('TWEETi3.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS techTWEETS")
    cur.execute("CREATE TABLE techTWEETS(author text, created int, tweet text)")
    consumer_key = "XODWe6MQRC34xwVYvIdOjrWpO"
    consumer_secret = "znh2cVXmQ2VSu4VH40gaxixtNKPXbkCfDaYZ8skcwyNQLSNPRf"
    access_token = "1506216229685579777-6XezVOCioXlaWlY4mbSlh7KIuRxeJi"
    access_secret_token = "eU6bmuzIhrozO7cg9bITJTN2pk0y7Mk3RkjXXt7Hb5Vi7"
    
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    
    auth.set_access_token(access_token, access_secret_token)
    api = tweepy.API(auth)
    # test authentication
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
        
    #https://www.techrepublic.com/article/25-tech-influencers-to-follow-on-twitter/
    
    for name in screen_names:
        tweets = api.user_timeline(screen_name = name, count=200)
        tweets=tweepy.Cursor(api.search_full_archive, label='techsearch',
        query="semiconductor OR semi-conductor OR TSMC OR intel OR INTEL or Taiwan", tweet_mode = 'extended').items(1000)
        # fetching statuses
        tweets = api.user_timeline(screen_name = name, count=200)
        for tweet in tweets:
            rowi = (tweet.author.screen_name, int(tweet.created_at.strftime("%Y%m%d")), tweet.text)
            cur.execute("INSERT OR IGNORE INTO techTWEETS VALUES( ?, ?, ?)",rowi)
    con.commit()
    
    #%%
    def sent_to_words(sentences):
        for sentence in sentences:
            # deacc=True removes punctuations
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))
    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc))
                 if word not in stop_words] for doc in texts]
    stop_words = stopwords.words('english')
    #%%

    
    tweets = pd.read_sql('SELECT tweet FROM techTWEETS',con)
    stop_words = stopwords.words('english')
    

    tweets['tweet_processed'] = \
    tweets['tweet'].map(lambda x: re.sub('[,\.!?]', '', x))
    # Remove urls
    tweets['tweet_processed'] = \
    tweets['tweet_processed'].map(lambda x: re.sub(r'http\S+', '', x))
    # Convert the titles to lowercase
    tweets['tweet_processed'] = \
    tweets['tweet_processed'].map(lambda x: x.lower())
    tweets['tweet_processed'] = remove_stopwords(tweets['tweet_processed'])
    for i in range(len(tweets['tweet_processed'])):
        tweets['tweet_processed'][i] = ' '.join([str(item) for item in tweets['tweet_processed'][i]])
    
    # Join the different processed tweets together.
    long_string = ','.join(list(tweets['tweet_processed'].values))
    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=5000, \
    contour_width=3, contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Technology Wordcloud')
    plt.axis("off")
    plt.show()
    
    data = tweets.tweet_processed.values.tolist()
    data_words = list(sent_to_words(data))
    # remove stop words
    data_words = remove_stopwords(data_words)
    id2word = corpora.Dictionary(data_words)# Create Corpus
    texts = data_words# Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    # number of topics
    num_topics = 2# Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
    num_topics=num_topics)
    print(lda_model.print_topics())

