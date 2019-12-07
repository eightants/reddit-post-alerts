# For hosting on Heroku we'll need to use the OS library to pull the Token 
# from the Enviroment Variables

import os
import random
import asyncio
import discord
import RedditScrape as rs
import psycopg2

import requests
from lxml import html
from selenium import webdriver
from time import sleep

# 11 for spring, 21 for summer, 31 for fall
term = "201911"
crn = "12359"
url = "https://compass-ssb.tamu.edu/pls/PROD/bwykschd.p_disp_detail_sched?term_in=" + term + "&crn_in=" + crn


subs = ['frugalmalefashion', 'freebies']
keywords = [['adidas', 'ultraboost', 'uniqlo', 'vans', 'nike', 'stan smith', 'a&f', 'abercrombie'], ['amazon']] #old keywords: alphabounce
channelid = 627214659719790594

token = os.environ['DISCORDBOT_TOKEN']
DATABASE_URL = os.environ['DATABASE_URL']

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(channelid)
    print(channel)
    # await client.wait_until_ready()
    while True: 
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # Creating a cursor (a DB cursor is an abstraction, meant for data set traversal)
        cur = conn.cursor()
        for i in range(len(subs)):
            sub = subs[i]
            posts = rs.ScrapePosts(sub, keywords[i])
            for p in posts:
                # Executing your PostgreSQL query
                cur.execute("SELECT EXISTS (SELECT 1 FROM redditpostalerts WHERE post_id = '" + str(p.id) + "');")
                post_id = cur.fetchone()[0]
                if post_id == False: 
                    cur.execute("INSERT INTO redditpostalerts (post_id) VALUES ('" + p.id + "');")
                    # In order to make the changes to the database permanent, we now commit our changes
                    conn.commit()
                    await channel.send("[" + sub + "] " + p.title + "\n" + p.url)
                #await channel.send(p.url)
        # checks tamu compass for space in classes
        res = requests.get(url)
        tree = html.fromstring(res.content)
        table = tree.xpath('//td/table[@class="datadisplaytable"]/tr/td/text()')
        cap = table[1]
        curr = table[2]
        if (cap > curr): 
            await channel.send("Space available in section: " + str(curr) + "/" + str(cap))
        # We have committed the necessary changes and can now close out our connection
        cur.close()
        conn.close()
        await asyncio.sleep(300)


client.run(token)