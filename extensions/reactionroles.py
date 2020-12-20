import discord
import configparser
from discord.ext.commands import Cog

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

class reactionroles(Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        guild = await self.client.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        config.read('./config.ini')
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
            if payload.emoji.name == "🇷🇺":  # russian role
                role = discord.utils.get(guild.roles, id=int(role_id['rus']))

                await member.add_roles(role)

                print('{} now has the role {}'.format(member,role))
            if payload.emoji.name == "🇫🇷":  # french role
                role = discord.utils.get(guild.roles, id=int(role_id['fra']))

                await member.add_roles(role)

                print('{} now has the role {}'.format(member,role))
            if payload.emoji.name == "🇪🇸":  # spanish role
                role = discord.utils.get(guild.roles, id=int(role_id['esp']))

                await member.add_roles(role)

                print('{} now has the role {}'.format(member,role))
            if payload.emoji.name == "🇨🇳":  # chinese role
                role = discord.utils.get(guild.roles, id=int(role_id['cn']))

                await member.add_roles(role)

                print('{} now has the role {}'.format(member,role))
            if payload.emoji.name == "🇮🇳":  # hindi role
                role = discord.utils.get(guild.roles, id=int(role_id['hin']))

                await member.add_roles(role)

                print('{} now has the role {}'.format(member,role))
            if payload.emoji.name == "🇰🇷":  # korean role
                role = discord.utils.get(guild.roles, id=int(role_id['kor']))

                await member.add_roles(role)

                print('{} now has the role {}'.format(member,role))
            if payload.emoji.name == "🇯🇵":  # japanese role
                role = discord.utils.get(guild.roles, id=int(role_id['jap']))

                await member.add_roles(role)

                print('{} now has the role {}'.format(member,role))

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        guild = await self.client.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        config.read('./config.ini')
        verify_id = int(config.get('MESSAGEID','verify'))
        lang_id = int(config.get('MESSAGEID', 'lang'))
        role_id = config['ROLEID']


        if message_id == verify_id:  # verification
            role = discord.utils.get(guild.roles, id=int(role_id['verified']))

            await member.remove_roles(role)

            embed = discord.Embed(
                title=config.get('UNVERIFIEDEMBED', 'title'),
                description=config.get('UNVERIFIEDEMBED', 'description'),
                colour=discord.Colour.blue()
            )
            await member.send(embed=embed)

            print('Role {} was removed from {}'.format(role, member))

        if message_id == int(lang_id):
            if payload.emoji.name == "🇩🇪":  # german role
                role = discord.utils.get(guild.roles, id=int(role_id['ger']))

                await member.remove_roles(role)

                print('Role {} was removed from {}'.format(role, member))
            if payload.emoji.name == "🇷🇺":  # russian role
                role = discord.utils.get(guild.roles, id=int(role_id['rus']))

                await member.remove_roles(role)

                print('Role {} was removed from {}'.format(role, member))
            if payload.emoji.name == "🇫🇷":  # french role
                role = discord.utils.get(guild.roles, id=int(role_id['fra']))

                await member.remove_roles(role)

                print('Role {} was removed from {}'.format(role, member))
            if payload.emoji.name == "🇪🇸":  # spanish role
                role = discord.utils.get(guild.roles, id=int(role_id['esp']))

                await member.remove_roles(role)

                print('Role {} was removed from {}'.format(role, member))
            if payload.emoji.name == "🇨🇳":  # chinese role
                role = discord.utils.get(guild.roles, id=int(role_id['cn']))

                await member.remove_roles(role)

                print('Role {} was removed from {}'.format(role, member))
            if payload.emoji.name == "🇮🇳":  # hindi role
                role = discord.utils.get(guild.roles, id=int(role_id['hin']))

                await member.remove_roles(role)

                print('Role {} was removed from {}'.format(role, member))
            if payload.emoji.name == "🇰🇷":  # korean role
                role = discord.utils.get(guild.roles, id=int(role_id['kor']))

                await member.remove_roles(role)

                print('Role {} was removed from {}'.format(role, member))
            if payload.emoji.name == "🇯🇵":  # japanese role
                role = discord.utils.get(guild.roles, id=int(role_id['jap']))

                await member.remove_roles(role)


                print('Role {} was removed from {}'.format(role, member))

def setup(client):
    client.add_cog(reactionroles(client))