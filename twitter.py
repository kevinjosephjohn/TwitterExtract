# File name: twitter.py
# Author: Kevin John
# Date created: 10/12/2015
# Date last modified: 4/25/2013
# Python Version: 2.7

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json
import smtplib
import requests
import re


#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username    MySQL pass  Database name.
conn = MySQLdb.connect("localhost","#######","#######d321","#######")

c = conn.cursor()


#consumer key, consumer secret, access token, access secret.
ckey="####"
csecret="###"
atoken="###-#"
asecret="####"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"].encode('ascii', 'ignore')
        retweetcount = all_data["retweet_count"]
        username = all_data["user"]["screen_name"].encode('ascii', 'ignore')
        tweet = str.lower(tweet)
        remove_list = ['RT', 'rt']
        word_list = tweet.split()
        tweet = ' '.join([i for i in word_list if i not in remove_list])
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
        # print((username,tweet))
        try:
            num_array=[int(s) for s in tweet.split() if s.isdigit()]
            for nu in num_array:
                num = str(nu)
                if (len(num) >= 10):
                 print num   
                 # c.execute("INSERT INTO requests (name, number, request, type) VALUES (%s,%s,%s,'twitter')",
                 # (username, num, tweet))          
                 r = requests.get('http://rainhelp.pyrumas.com/processwhatsapp.php?text='+tweet+'&number='+num+'&source=twitter&name='+username+'&type=S')  
                 serverresponse = r.text    
                 print((username,tweet,serverresponse))

        except MySQLdb.IntegrityError:
            pass  # or may be at least log?
        conn.commit()

        
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["chennaimicro,chennaifloods,chennairainshelp"])
