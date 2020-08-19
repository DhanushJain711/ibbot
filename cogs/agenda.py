import discord
from discord.ext import commands

import sqlite3

conn = sqlite3.connect('agendas.db')
c = conn.cursor()
#c.execute("""CREATE TABLE agendas (
#            code integer,
#            item text
#            ) """)

def add_item(code, item):
    with conn:
        c.execute("INSERT INTO agendas VALUES (:code, :item)" ,
                    {'code' : code, 'item' : item})

def get_items(code):
    c.execute("SELECT item FROM agendas WHERE code=:code", {'code': code})
    return c.fetchall()

def remove_item(code, item):
    with conn:
        c.execute("DELETE from agendas WHERE code = :code AND item = :item",
                    {'code': code , 'item': item})


class Agenda(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("agenda bot loaded")

    @commands.group(invoke_without_command = True)
    async def agenda(self, ctx):
        await ctx.send("Add to agenda, list agenda, or remove from agenda")

    @agenda.command()
    async def add(self, ctx, *, item):
        author = str(ctx.author)
        code = int(author[-4:])
        add_item(code, item)
        items = get_items(code)
        await ctx.send(""" Added "{}" to {}'s agenda. You currently have {} item(s) in you agenda. """.format(item, author[:-5], len(items)))

    @agenda.command()
    async def remove(self, ctx, *, item):
        author = str(ctx.author)
        code = int(author[-4:])
        remove_item(code, item)

    @agenda.command()
    async def list(self, ctx):
        author = str(ctx.author)
        code = int(author[-4:])
        items = get_items(code)
        if len(items) == 0:
            await ctx.send('Your list is currently empty. Use "agenda add" to add to your agenda')
        else:
            message = "{}'s agenda: \n".format(author[:-5])
            for i in range(len(items)):
                message += "Item {}. {} \n".format(i+1 , items[i][0])
            await ctx.send(message)

def setup(client):
    client.add_cog(Agenda(client))
