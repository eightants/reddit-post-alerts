import praw
import pdb
import re
import os
import time
from datetime import datetime, timedelta

subs = ['spotify']
keywords = ['player', 'playlist']

def ScrapePosts(subs, keywords):
    posts = []
    for sub in subs:
        try:

            username = os.environ['BOTONE_USERNAME']
            password = os.environ['BOTONE_PASSWORD']
            client_id = os.environ['BOTONE_ID']
            client_secret = os.environ['BOTONE_SECRET']
            user_agent = os.environ['BOTONE_AGENT']
            
            reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, username=username, user_agent=user_agent)
            #reddit = praw.Reddit(client_id="ffyfOn7R40octw", client_secret="eQ_8GAD7K-oUeA8W44anLmEn1l0", password="thevacation", username="askreddit-sim", user_agent="redditscrape-v1")

            subreddit = reddit.subreddit(sub)

            # checks for any new post
            for submission in subreddit.new(limit=5):
                for keyword in keywords:
                    if submission.title.lower().find(keyword) != -1: 
                        posts.append(submission)
                        break
            time.sleep(5)            
        except Exception as e: 
            time.sleep(10)
    return posts
