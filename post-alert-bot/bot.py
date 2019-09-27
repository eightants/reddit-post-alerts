# For hosting on Heroku we'll need to use the OS library to pull the Token 
# from the Enviroment Variables

import os
import random
import asyncio
import discord
import RedditScrape as rs

# read config file
subs = ['frugalmalefashion']
keywords = ['adidas', 'ultraboost', 'uniqlo']
channelid = 627214659719790594

token = os.environ['DISCORDBOT_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(channelid)
    print(channel)
    # await client.wait_until_ready()
    while True:
        for sub in subs:
            posts = rs.ScrapePosts(sub, keywords)
            for p in posts:
                await channel.send("[" + sub + "] " + p.title + "\n" + p.url)
                #await channel.send(p.url)
        await asyncio.sleep(1200)


client.run(token)