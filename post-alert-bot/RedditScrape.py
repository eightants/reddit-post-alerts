import praw
import pdb
import re
import os
import time
from datetime import datetime, timedelta


def ScrapePosts(sub, keywords):
    posts = []
    try:
        username = os.environ['BOTONE_USERNAME']
        password = os.environ['BOTONE_PASSWORD']
        client_id = os.environ['BOTONE_ID']
        client_secret = os.environ['BOTONE_SECRET']
        user_agent = os.environ['BOTONE_AGENT']

        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, username=username, user_agent=user_agent)

        subreddit = reddit.subreddit(sub)

        # checks for any new post
        for submission in subreddit.new(limit=10):
                for keyword in keywords:
                    if submission.title.lower().find(keyword) != -1: 
                        posts.append(submission)
                        print("Match for" + keyword + ": " + submission.title)
                        break
        time.sleep(2)            
    except Exception: 
        time.sleep(10)
    return posts
