# For hosting on Heroku we'll need to use the OS library to pull the Token 
# from the Enviroment Variables

import os
import random
import asyncio
import discord
import RedditScrape as rs
import psycopg2

# read config file
subs = ['frugalmalefashion']
keywords = ['adidas', 'ultraboost', 'uniqlo']
channelid = 627214659719790594

token = os.environ['DISCORDBOT_TOKEN']
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(channelid)
    print(channel)
    # await client.wait_until_ready()
    while True: 
        # Creating a cursor (a DB cursor is an abstraction, meant for data set traversal)
        cur = conn.cursor()
        for sub in subs:
            posts = rs.ScrapePosts(sub, keywords)
            for p in posts:
                # Executing your PostgreSQL query
                cur.execute("SELECT EXISTS (SELECT 1 FROM redditpostalerts WHERE post_id = '" + str(p.id) + "');")
                post_id = cur.fetchone()[0]
                print(post_id)
                if post_id == False: 
                    cur.execute("INSERT INTO redditpostalerts (post_id) VALUES ('" + p.id + "');")
                    # In order to make the changes to the database permanent, we now commit our changes
                    conn.commit()
                    await channel.send("[" + sub + "] " + p.title + "\n" + p.url)
                #await channel.send(p.url)
        # We have committed the necessary changes and can now close out our connection
        cur.close()
        conn.close()
        await asyncio.sleep(300)


client.run(token)