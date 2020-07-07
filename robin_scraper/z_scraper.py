import requests
import webbrowser
import json
from twython import Twython
import pandas as pd
import re
import praw
import nltk #do we still need this? Probs a fair amount of these not needed
import unicodedata
from bs4 import BeautifulSoup

# def main():
#     # testtw = twitter_api_and_cleaner('chicken fried')
#     # print(testtw.search(50, 10, 5, 10))
#     #
#     # testre = reddit_api_and_cleaner('chicken fried')
#     # print(testre.search(50,60,5,10))
#     #for twitter, cutoff around 10 seems reasonable
#     testwi = wikipedia_api_and_cleaner('chicken fried')
#     print(testwi.search(10,2,1,10)) #we gonna need to optimize these paramaters, ncutoff should always be 1 for wikipedia
class api_and_cleaner:
    def __init__(self,exactText,auth_holder):
        self.exactTerm = exactText
        self.t_consumer_key = auth_holder.t_consumer_key
        self.t_consumer_secret= auth_holder.t_consumer_secret
        self.t_access_token = auth_holder.t_access_token
        self.t_access_secret = auth_holder.t_access_secret
        self.r_client_id = auth_holder.r_client_id
        self.r_client_secret = auth_holder.r_client_secret
        self.r_username = auth_holder.r_username
        self.r_password = auth_holder.r_password

    def cleanText(self,text):
        text.replace("’", "'")
        text = ''.join(c for c in unicodedata.normalize('NFC', text) if c <= '\uFFFF')
        toRet = ''.join(c for c in text if c <= '\uFFFF')
        toRet = re.sub('(RT )?@(\w)*:?\s', '', toRet)
        toRet = re.sub('(https://t)','', toRet)
        toRet = re.sub('(\w)*:\w', '', toRet)
        # Replace HTML Character Entities
        toRet = re.sub('&amp;', '&', toRet)
        toRet = re.sub('&gt;', '>', toRet)
        toRet = re.sub('&lt;', '<', toRet)
        toRet = re.sub('&nbsp;', ' ', toRet)
        toRet = re.sub('&quot;', '\"', toRet)
        toRet = re.sub('&apos;', '\'', toRet)
        
        toRet = toRet.strip()
        toRet = re.split('[(\.|\?|!)\n]', toRet)
        return list(filter(None, toRet))
    # def remove_whitespace_and_craziness(self,sentence): #unused function
    #     toRet = re.split('[,@#:\'\:; ?!~_   ]', sentence)
    #     return list(filter(None, toRet))

    def process_json(self,howManyToQuery):
        return [],5,10

    def decide_confidence(self,n, avg, cutoff, ncutoff):
        if (avg < cutoff or n < ncutoff):
            return 'likely unreliable'
        else:
            return 'likely reliable'

    def search(self,howManyToQuery,cutoff,ncutoff,dispcutoff):
        jsonStuff = self.get_json(howManyToQuery)

        toRet, metricTotal, n = self.process_json(jsonStuff,dispcutoff)

        if not n == 0:
            print('metric avg: ', metricTotal / n)
            return toRet, self.decide_confidence(n, metricTotal / n, cutoff, ncutoff), metricTotal / n
        return {}, 'No results: unreliable', 0

class twitter_api_and_cleaner(api_and_cleaner):
    def get_json(self,howManyToQuery):
        python_tweets = Twython(self.t_consumer_key, self.t_consumer_secret)
        query = {'q': '"' + self.exactTerm + '"',
                 'count': howManyToQuery,
                 'lang': 'en'
                 }
        return python_tweets.search(**query)

    def process_json(self,jsonStuff,dispcutoff):
        sentences = {}
        retweetTotal = 0
        test = []
        for tweet in jsonStuff['statuses']:
            for sent in self.cleanText(tweet['text']):
                if (self.exactTerm.lower() in sent.lower()):
                    if not sent.strip().lower() == self.exactTerm.lower():
                        test.append(sent.strip())
                        retweetTotal += tweet['retweet_count']  # go back to fix l8r
                        sentences[sent.strip()] = tweet['retweet_count']
        # now lets turn lists into strings
        sentences = {k: v for k, v in sorted(sentences.items(), key=lambda item: item[1], reverse=True)}
        toRet = [key for key in list(sentences.keys())[0:dispcutoff]] #confirmed to work

        return (toRet, retweetTotal, len(sentences))


class reddit_api_and_cleaner(api_and_cleaner):
    def get_json(self,howManyToQuery):
        sentences = {}
        reddit = praw.Reddit(client_id=self.r_client_id, \
                             client_secret=self.r_client_secret, \
                             user_agent='texter', \
                             username=self.r_username, \
                             password=self.r_password)
        all = reddit.subreddit('all')
        return all.search(self.exactTerm, limit=howManyToQuery)

    def process_json(self, jsonStuff, dispcutoff):
        upvoteTotal = 0
        sentences = {}
        for i in jsonStuff:
            for sent in self.cleanText(i.title):
                if (self.exactTerm.lower() in sent.lower()):
                    upvoteTotal += i.score
                    sentences[sent] = i.score
        sentences = {k: v for k, v in sorted(sentences.items(), key=lambda item: item[1], reverse=True)}
        toRet = [key for key in list(sentences.keys())[0:dispcutoff]]  # confirmed to work

        return (toRet, upvoteTotal, len(sentences))

class wikipedia_api_and_cleaner(api_and_cleaner):
    def get_json(self,howManyToQuery):
        resp = requests.get('http://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch='+self.exactTerm+'&srlimit='+str(howManyToQuery))
        return resp.json()

    def process_json(self, jsonStuff, dispcutoff):
        is_contained = 0
        valid_examples = []
        for result in jsonStuff['query']['search']:
            if len(valid_examples) <= dispcutoff:
                if (self.exactTerm.lower() in BeautifulSoup(result['snippet'], 'html.parser').text.lower()):
                    is_contained += 1
                    valid_examples.append(BeautifulSoup(result['snippet'], 'html.parser').text)
                elif (self.exactTerm.lower() in result['title'].lower()):
                    is_contained += 1
        return (valid_examples, is_contained, 1) #n=1 because is_contained is the deciding metric


        print('number of exact matches capitalization insensitive:', is_contained)
        print('deem to be likely:', is_contained >= instances_until_likely)

def get_informal(twitt,redd):
    t_low = 100
    r_low = 100
    t_high = 600
    r_high = 600
    if (twitt >= t_low and redd >= r_low) or (twitt >= t_high or redd >= r_high):
        return "Likely"
    elif twitt >= t_low or redd >= r_low:
        return "Inconclusive"
    return "Unlikely"
def get_formal(wiki):
    w_cut = 2
    if wiki > w_cut:
        return "Likely"
    if wiki == w_cut:
        return "Inconclusive"
    return "Unlikely"
# main()
