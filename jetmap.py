#!/usr/bin/env python3

# TODO:
# check if CSV exists before writing header row
# do check if RT properly
# add output to Slack channel
# extract defanged URLs and convert for #opendir matches

import tweepy
import sys
import configparser
import json
import csv
import signal

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DATA']['api_key']
api_secret = config['DATA']['api_secret']
access_token = config['DATA']['access_token']
access_secret = config['DATA']['access_secret']

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if (not tweet.retweeted) and (not tweet.text.startswith('RT ')):
            created = tweet.created_at.strftime("%Y-%m-%d-%H:%M:%S")
            final_urls = []
            url_output = []
            sep = '\t' # tab separator for f-string URL output. See https://stackoverflow.com/a/44780467
            # check if long form tweet > 140 characters.
            if hasattr(tweet, 'extended_tweet'):
                tweet_text = clean_tweet(tweet.extended_tweet['full_text'])
                url = tweet.extended_tweet['entities']['urls']
                # check if there are URLs in the tweet
                if not url:
                    print(f"Username: {tweet.user.name}\nAccount: {tweet.user.screen_name}\nTimestamp: {created} UTC\nTwitter ID: {tweet.id_str}\nFull Text: {tweet_text}\nURL: nil")
                # if there are URLs loop through their list and print via list comprehension. See https://stackoverflow.com/a/52006459
                else:
                    url = tweet.extended_tweet['entities']['urls']
                    for dic in url:
                        for key in dic:
                            if key == 'expanded_url':
                                final_urls.append(dic[key])
                    url_output = sep.join([ref for ref in final_urls])
                    print(f"Username: {tweet.user.name}\nAccount: {tweet.user.screen_name}\nTimestamp: {created} UTC\nTwitter ID: {tweet.id_str}\nFull Text: {tweet_text}\nURL: {url_output}")
            else: 
                tweet_text = clean_tweet(tweet.text)
                url = tweet.entities['urls']
                if not url:
                    print(f"Username: {tweet.user.name}\nAccount: {tweet.user.screen_name}\nTimestamp: {created} UTC\nTwitter ID: {tweet.id_str}\nText: {tweet_text}\nURL: nil")
                else:
                    url = tweet.entities['urls']
                    for dic in url:
                        for key in dic:
                            if key == 'expanded_url':
                                final_urls.append(dic[key])
                    url_output = sep.join([ref for ref in final_urls])
                    print(f"Username: {tweet.user.name}\nAccount: {tweet.user.screen_name}\nTimestamp: {created} UTC\nTwitter ID: {tweet.id_str}\nText: {tweet_text}\nURL: {url_output}")
            print("\n\n\n\n")
            write_csv_body(created, tweet.user.screen_name, tweet.user.name, tweet.id_str, tweet_text, url_output)

    def on_error(self, status):
        print("Error detected")

def write_csv_header():
    with open('output.csv', mode='w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        writer.writerow(['Timestamp', 'Username', 'Account Name', 'Twitter ID', 'Tweet Text', 'URL 1', 'URL 2', 'URL 3', 'URL 4', 'URL 5', 'URL 6'])
    file.close()

def write_csv_body(*data):
    with open('output.csv', mode='a', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        writer.writerow(data)
    file.close()
    
def clean_tweet(text):
    clean_tweet_text = text.replace('\n', ' ').replace('\r', '').replace('\xa0', ' ') # \xa0 = non-breaking space but appears as unicode in tweet API output.
    return(clean_tweet_text)

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Exit.".format(signal))
    exit(0)

def main():
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    write_csv_header()
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(follow=["861230178164498433"], track=['#opendir', '#malware'])

if __name__== "__main__":
    main()