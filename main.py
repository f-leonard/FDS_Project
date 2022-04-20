# -*- coding: utf-8 -*-

"""
Created on Sat Mar  5 14:47:51 2022

@author: 35387
"""
#%%
import tweepy
import sqlite3 as lite
import nltk
import pandas as pd
import gensim
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from pprint import pprint
import tweepy
import time
#%%

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
#%%
def scrape(words,date_since,numtweet):
    time.sleep(0.01)
    db = pd.DataFrame(columns = ['username',
                                 'description',
                                 'location',
                                 'text',
                                 'hashtags'])
    tweets = tweepy.Cursor(api.search_tweets,words,lang = 'en',
                           since_id = date_since,
                           tweet_mode = 'extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    i = 1
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        
        hashtags = tweet.entities['hashtags']
 
        # Retweets can be distinguished by
        # a retweeted_status attribute,
        # in case it is an invalid reference,
        # except block will be executed
        try:
                text = tweet.retweeted_status.full_text
        except AttributeError:
                text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
                hashtext.append(hashtags[j]['text'])
 
        # Here we are appending all the
        # extracted information in the DataFrame
        ith_tweet = [username, description,
                     location, text, hashtext]
        db.loc[len(db)] = ith_tweet
 
        # Function call to print tweet data on screen
        i = i+1
    filename = 'TSMC_supply.csv'
 
        # we will save our database as a CSV file.
    db.to_csv(filename)

scrape(['supply chain','TSMC',],20200101,1000)
#%%
#https://www.techrepublic.com/article/25-tech-influencers-to-follow-on-twitter/
'''screen_names = ['@','@Boeing','@Airbus']
for name in screen_names:
    tweets = api.user_timeline(screen_name = name, count=1000)
    tweets=tweepy.Cursor(api.search_full_archive, label='techsearch',
                         query="semiconductor OR technology", tweet_mode = 'extended').items(1000)
# fetching statuses
    tweets = api.user_timeline(screen_name = name, count=1000)
    for tweet in tweets:
        rowi = (tweet.author.screen_name, int(tweet.created_at.strftime("%Y%m%d")), tweet.text)
        cur.execute("INSERT OR IGNORE INTO techTWEETS VALUES( ?, ?, ?)",rowi)
con.commit()'''
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
if __name__ == '__main__':
    tweets = pd.read_csv('rusukr.csv')
    tweets = tweets.drop_duplicates(subset ='text', keep = 'first')
    
    stop_words = stopwords.words('english')
    stop_words.extend(['visit','lawmakers','taiwan','china','surprise','arrive'])
    
    tweets['tweet_processed'] = \
    tweets['text'].map(lambda x: re.sub('[,\.!?]', '', x))
    # Remove urls
    tweets['tweet_processed'] = \
    tweets['tweet_processed'].map(lambda x: re.sub(r'http\S+', '', x))
    # Convert the titles to lowercase
    tweets['tweet_processed'] = \
    tweets['tweet_processed'].map(lambda x: x.lower())
    tweets['tweet_processed'] = remove_stopwords(tweets['tweet_processed'])
    #for i in range(len(tweets['tweet_processed'])):
        #tweets['tweet_processed'][i] = ' '.join([str(item) for item in tweets['tweet_processed']])# Join the different processed tweets together.
    #print(','.join(tweets['tweet_processed'][0]))
    listlist =list(tweets['tweet_processed'].values)
    long_list = [item for sublist in listlist for item in sublist]
    long_list =list(filter(('rt').__ne__, long_list))
    print(long_list)
    long_string = ','.join(long_list)
    # Create a WordCloud object
    
    wordcloud = WordCloud(background_color="white", max_words=5000, \
    contour_width=5, contour_color='steelblue')
    # Generate a word cloud
    wordcloud.generate(long_string)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    
    plt.axis("off")
    plt.show()

    
    data = tweets.tweet_processed.values.tolist()
    data_words = list(sent_to_words(data))
    # remove stop words
    data_words = remove_stopwords(data_words)
    id2word = corpora.Dictionary(data_words)# Create Corpus
    
    texts = data_words
    print(texts)
    corpus = [id2word.doc2bow(text) for text in texts]
    # number of topics
    num_topics = 5# Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
    id2word=id2word,
    num_topics=num_topics)
    pprint(lda_model.print_topics())

#%%
    def format_topics_sentences(ldamodel=None, corpus=corpus, texts=data):
        # Init output
        sent_topics_df = pd.DataFrame()
    
        # Get main topic in each document
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list            
            # print(row)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
    
        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        return(sent_topics_df)
    
    
    df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=texts)
    
    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    
