import discord
from discord.ext import commands

class Sqlbot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Sqlbot loaded')

    @commands.command()
    async def bruh(self, ctx):
        await ctx.send('bruh')

    @commands.command()
    async def create(self, ctx, *, info):



def setup(client):
    client.add_cog(Sqlbot(client))
