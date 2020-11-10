import tweepy
import logging
import time
import sys
import requests
import os
import random
import glob
# I put my keys in the keys.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.
from keys_format import *

print('this is my twitter bot')
#Made a file with ur tweet bot keys 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

abspath = os.path.abspath(__file__)
dname = os.path.dirname("C:\Users\Pc\Desktop\mybot\*") #Here put your route to the folder
os.chdir(dname)
print(dname)

FILE_NAME = 'last_seen_id.txt' #temp file to save last seen tweet id

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
	
    print('retrieving and replying to tweets...')
    #use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    folder = "C:\Users\Pc\Desktop\mybot\images\*" #Path where ur images or gifs are saved
    images = glob.glob(folder + "*")
    image_open = images[random.randint(0,len(images))-1]
	
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
	#reversed for reply to the oldest tweet first
    for mention in reversed(mentions):
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#perfume' in mention.full_text.lower():
            print('found #perfume')
            print('responding back...')
            m = " Pls support perfume " 
            pic = api.media_upload(image_open)
            api.update_status('@' + mention.user.screen_name + m, mention.id, media_ids = [pic.media_id_string])

while True:
    reply_to_tweets()
    time.sleep(15)