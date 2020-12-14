import discord
import configparser
from pycoingecko import CoinGeckoAPI
from configparser import ConfigParser
from discord.ext import commands

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
cg = CoinGeckoAPI()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)


@client.event
async def on_ready():
    print('You have logged in as {0.user}'.format(client))
    client.loop.create_task(status_task())


async def status_task():
    await client.change_presence(activity=discord.Game('HODLing QKC'), status=discord.Status.online)

@client.event
async def on_member_join(member):
    channel_id = 787082086094864464

    embed = discord.Embed(
        title='Welcome to the official QuarkChain Discord server!',
        description='To verify go to #[{}](https://discord.gg/pUSXaYq9vN), read through the rules and react to the bottom message.'.format(client.get_channel(channel_id)),
        color=discord.Colour.blue()
    )

    await member.send(embed=embed)
    print('User {} joined our server'.format(member))


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    config.read('config.ini')
    verify_id = int(config.get('MESSAGEID', 'verify'))
    lang_id = int(config.get('MESSAGEID', 'lang'))
    role_id = config['ROLEID']

    if message_id == verify_id:  # verification
        role = discord.utils.get(guild.roles, id=int(role_id['verified']))

        await member.add_roles(role)

        verifemb = config['VERIFIEDEMBED']
        embed = discord.Embed(
            title=verifemb['title'],
            colour=discord.Colour.blue()
        )

        await member.send(embed=embed)

        print('User {} is now verified'.format(member))

    if message_id == lang_id:
        if payload.emoji.name == "🇩🇪":  # german role
            role = discord.utils.get(guild.roles, id=int(role_id['ger']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
        if payload.emoji == "🇷🇺":  # russian role
            role = discord.utils.get(guild.roles, id=int(role_id['rus']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
        if payload.emoji == "🇫🇷":  # french role
            role = discord.utils.get(guild.roles, id=int(role_id['fra']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
        if payload.emoji == "🇪🇸":  # spanish role
            role = discord.utils.get(guild.roles, id=int(role_id['esp']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
        if payload.emoji == "🇨🇳":  # chinese role
            role = discord.utils.get(guild.roles, id=int(role_id['cn']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
        if payload.emoji == "🇮🇳":  # hindi role
            role = discord.utils.get(guild.roles, id=int(role_id['hin']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
        if payload.emoji == "🇰🇷":  # korean role
            role = discord.utils.get(guild.roles, id=int(role_id['kor']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
        if payload.emoji == "🇯🇵":  # japanese role
            role = discord.utils.get(guild.roles, id=int(role_id['jap']))

            await member.add_roles(role)

            print('{} now has the role {}'.format(member,role))
@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    config.read('config.ini')
    verify_id = int(config.get('MESSAGEID','verify'))
    lang_id = int(config.get('MESSAGEID', 'lang'))
    role_id = config['ROLEID']


    if message_id == verify_id:  # verification
        role = discord.utils.get(guild.roles, id=int(role_id['verified']))

        await member.remove_roles(role)

        embed = discord.Embed(
            title=config.get('UNVERIFIEDEMBED','title'),
            description=config.get('UNVERIFIEDEMBED','description'),
            colour=discord.Colour.blue()
        )
        await member.send(embed=embed)

        print('Role {} was removed from {}'.format(role, member))

    if message_id == int(lang_id):
        if payload.emoji.name == "🇩🇪":  # german role
            role = discord.utils.get(guild.roles, id=int(role_id['ger']))

            await member.remove_roles(role)

            print('Role {} was removed from {}'.format(role, member))
        if payload.emoji == "🇷🇺":  # russian role
            role = discord.utils.get(guild.roles, id=int(role_id['rus']))

            await member.remove_roles(role)

            print('Role {} was removed from {}'.format(role, member))
        if payload.emoji == "🇫🇷":  # french role
            role = discord.utils.get(guild.roles, id=int(role_id['fra']))

            await member.remove_roles(role)

            print('Role {} was removed from {}'.format(role, member))
        if payload.emoji == "🇪🇸":  # spanish role
            role = discord.utils.get(guild.roles, id=int(role_id['esp']))

            await member.remove_roles(role)

            print('Role {} was removed from {}'.format(role, member))
        if payload.emoji == "🇨🇳":  # chinese role
            role = discord.utils.get(guild.roles, id=int(role_id['cn']))

            await member.remove_roles(role)

            print('Role {} was removed from {}'.format(role, member))
        if payload.emoji == "🇮🇳":  # hindi role
            role = discord.utils.get(guild.roles, id=int(role_id['hin']))

            await member.remove_roles(role)

            print('Role {} was removed from {}'.format(role, member))
        if payload.emoji == "🇰🇷":  # korean role
            role = discord.utils.get(guild.roles, id=int(role_id['kor']))

            await member.remove_roles(role)

            print('Role {} was removed from {}'.format(role, member))
        if payload.emoji == "🇯🇵":  # japanese role
            role = discord.utils.get(guild.roles, id=int(role_id['jap']))

            await member.remove_roles(role)


            print('Role {} was removed from {}'.format(role, member))


@client.command(aliases=['c'])
async def crypto(ctx, *, symbol):
    print(cg.get_price(ids=symbol, vs_currencies='usd'))
    await ctx.send(cg.get_price(ids=symbol, vs_currencies='usd'))

@client.command()
async def addReaction(ctx, msgID: int, emoji):
    guild = ctx.message.guild
    msg = await ctx.fetch_message(msgID)
    await msg.add_reaction(emoji)
    print('{} added a reaction to message {} via the bot'.format(ctx.message.author,ctx.message))
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