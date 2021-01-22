import discord
import tweepy
import configparser
import asyncio
from discord.ext import commands
import os
from datetime import datetime
import logging

logging.basicConfig(filename="bot.log", level=logging.INFO)

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
client = commands.Bot(command_prefix='-', intents=discord.Intents.all())

auth = tweepy.OAuthHandler("mine", "mine")
auth.set_access_token("mine", "mine")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class streamListener(tweepy.StreamListener):

    def __init__(self, discord, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discord = discord
        self.loop = loop

    def on_status(self, tweet):
        if tweet.user.id == 973766864659734528:
            print(f'[{datetime.now()}]Tweet from {tweet.user.name} detected')
            logging.info(f'[{datetime.now()}]Tweet from {tweet.user.name} detected')
            self.send_message(tweet.id, tweet.user.name)
        else:
            print(f'[{datetime.now()}]Retweet/reply by user {tweet.user.name}')
            logging.info(f'[{datetime.now()}]Retweet/reply by user {tweet.user.name}')

    def on_error(self, status):
        print(f'[{datetime.now()}][Tweepy]Error {status} detected')

    def send_message(self, msg, name):
        future = asyncio.run_coroutine_threadsafe(self.discord(msg, name), self.loop)
        future.result()

@client.event
async def on_ready():
    print(f'[{datetime.now()}]You have logged in as {client.user}')
    logging.info(f'[{datetime.now()}]You have logged in as {client.user}')
    client.loop.create_task(status_task())

    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            client.load_extension(f'extensions.{filename[:-3]}')

    tweet_listener = streamListener(discord=sendTweet, loop=asyncio.get_event_loop())
    stream = tweepy.Stream(api.auth, tweet_listener)
    stream.filter(follow=[str(config.get('TWITTER', 'account'))], is_async=True)

async def sendTweet(tweet_id, tweet_name):
    channel = await client.fetch_channel(config.get('CHANNELID', 'announcements'))
    guild = await client.fetch_guild(config.get('GUILDID', 'main'))
    url = f'https://twitter.com/{str(tweet_name)}/status/{str(tweet_id)}'
    await channel.send(f'{guild.default_role} check out our latest update:\n'
                       f'{url}')
    print(f'[{datetime.now()}]Tweet was successfully announced')
    logging.info(f'[{datetime.now()}]Tweet was successfully announced')

async def status_task():
    await client.change_presence(activity=discord.Game('HODLing QKC'), status=discord.Status.online)

@client.event
async def on_member_join(member):

    embed = discord.Embed(
        title=config.get('WELCOMEEMBED', 'title'),
        description=config.get('WELCOMEEMBED', 'description'),
        color=discord.Colour.blue()
    )

    await member.send(embed=embed)
    print(f'[{datetime.now()}]User {member} joined the server')
    logging.info(f'[{datetime.now()}]User {member} joined the server')

@client.event
async def on_member_remove(member):
    print(f'[{datetime.now()}]User {member} left the server')
    logging.info(f'[{datetime.now()}]User {member} left the server')



config.read('config.ini')
client.run(config.get('DISCORD', 'bottoken'))
