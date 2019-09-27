# For hosting on Heroku we'll need to use the OS library to pull the Token 
# from the Enviroment Variables

import os
import random
import asyncio
import discord
import RedditScrape as rs

token = os.environ['DISCORDBOT_TOKEN']

client = discord.Client()
subs = ['frugalmalefashion']
keywords = ['adidas', 'ultraboost']

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(326332285802774538)
    print(channel)
    # await client.wait_until_ready()
    while True:
        posts = rs.ScrapePosts(subs, keywords)
        for p in posts:
            await channel.send("[" + p.subreddit.name + "] " + p.title + "\n" + p.url)
            #await channel.send(p.url)
        await asyncio.sleep(60)


client.run(token)