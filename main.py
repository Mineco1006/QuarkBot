import discord
import tweepy
import configparser
import asyncio
from discord.ext import commands
import os

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
client = commands.Bot(command_prefix='-', intents=discord.Intents.all())

auth = tweepy.OAuthHandler("clM3nhJHc2GeuFIQ1mWUuGFSa", "IbTqzO9CkBILtKJ0DPTtkFKpCUOb06ys3fe2vCWvyxSkTF7mtn")
auth.set_access_token("1337413337286631426-t3mXEtBmW9310IDUCdXYGD68u65oV8", "mAUV3fcfImtPEWrlYRe22Q9kSwHkvRIODaRB5hDNNPxBR")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class streamListener(tweepy.StreamListener):

    def __init__(self, discord, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discord = discord
        self.loop = loop

    def on_status(self, tweet):
        print(f'Tweet from {tweet.user.name} detected')
        self.send_message(tweet.id)

    def on_error(self, status):
        print(f'Error {status} detected')

    def send_message(self, msg):
        future = asyncio.run_coroutine_threadsafe(self.discord(msg), self.loop)
        future.result()

@client.event
async def on_ready():
    print('You have logged in as {0.user}'.format(client))
    client.loop.create_task(status_task())

    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            client.load_extension(f'extensions.{filename[:-3]}')

    tweet_listener = streamListener(discord=sendTweet, loop=asyncio.get_event_loop())
    stream = tweepy.Stream(api.auth, tweet_listener)
    stream.filter(follow=['1337413337286631426'], is_async=True)

async def sendTweet(tweet_id):
    channel = await client.fetch_channel(config.get('CHANNELID', 'announcements'))
    guild = await client.fetch_guild(config.get('GUILDID', 'main'))
    url = f'https://twitter.com/twitter/statuses/{str(tweet_id)}'

    await channel.send(f'{guild.default_role} check out our latest update:\n'
                       f'{url}')
    print(f'Tweet was successfully announced')

async def status_task():
    await client.change_presence(activity=discord.Game('HODLing QKC'), status=discord.Status.online)

@client.event
async def on_member_join(member):
    channel_id = 787082086094864464

    embed = discord.Embed(
        title='Welcome to the official QuarkChain Discord server!',
        description='To verify go to #[{}](https://discord.gg/pUSXaYq9vN), read the rules and react to the bottom message.'.format(client.get_channel(channel_id)),
        color=discord.Colour.blue()
    )

    await member.send(embed=embed)
    print('User {} joined our server'.format(member))

@client.command()
async def addReaction(ctx, msgID: int, emoji):
    msg = await ctx.fetch_message(msgID)
    await msg.add_reaction(emoji)
    print('{} added a reaction to message {} via the bot'.format(ctx.message.author, ctx.message))
@client.command()
async def reactionMessage(ctx, type):
    channel = ctx.message.channel
    guild = ctx.message.guild
    if type == 'lang':
        langembed = config['LANGEMBED']
        langemb = discord.Embed(
            title=langembed['title'],
            description=langembed['description'],
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=langemb)
    elif type == 'verify':
        verifyembed = config['VERIFYEMBED']
        veremb = discord.Embed(
            title=verifyembed['title'],
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=veremb)


config.read('config.ini')
client.run(config.get('DISCORD','bottoken'))