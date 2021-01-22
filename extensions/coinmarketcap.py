import discord
from discord.ext import commands
import configparser
from coinmarketcapapi import CoinMarketCapAPI
import locale
from datetime import datetime
import logging

logging.basicConfig(filename=".bot.log", level=logging.INFO)

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read('./config.ini')
cmc = CoinMarketCapAPI(config.get('CMC', 'apikey'))
locale.setlocale(locale.LC_ALL, '')

class coinmarketcap(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['c'])
    async def crypto(self, ctx, *, symbol):
        r = cmc.cryptocurrency_quotes_latest(symbol=symbol)
        d = r.data.get(symbol.upper())
        u = d.get("quote").get("USD")
        name = d.get('name')
        print(f'[{datetime.now()}]Cryptocurrency quote {name} requested by {ctx.message.author}')
        logging.info(f'[{datetime.now()}]Cryptocurrency quote {name} requested by {ctx.message.author}')

        embed= discord.Embed(
            title=d.get('name').upper(),
            description='Price: ${}\n'
                        'Volume 24h: ${}\n'
                        'Change 24h: {}%\n'
                        'Supply: {} {}\n'
                        'Market capitalization: ${}\n'.format(locale.format_string('%.4f', float(u.get("price")), grouping=True),
                                                            locale.format_string('%.2f', float(u.get("volume_24h")), grouping=True),
                                                            locale.format_string('%.2f', float(u.get("percent_change_24h"))),
                                                            locale.format_string('%.0f', float(d.get("circulating_supply")), grouping=True),
                                                            d.get("symbol"),
                                                            locale.format_string('%.0f', float(u.get("market_cap")), grouping=True)),
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(coinmarketcap(client))
