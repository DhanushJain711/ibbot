import discord
from discord.ext import commands

import sqlite3

conn = sqlite3.connect('sqlbot.db')

c = conn.cursor()

# c.execute("""CREATE TABLE employees (
#             first text,
#             last text,
#             pay integer
#            )""")

def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)" ,
                    {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchone()

def update_pay(last,pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE last = :last""",
                    {'last': last, 'pay': pay})

def remove_emp(first):
    with conn:
        c.execute("DELETE from employees WHERE first = :first",
                    {'first': first})

class Employee:

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    def email(self):
        return f'{self.first.lower()}.{self.last.lower()}@email.com'

    def fullname(self):
        return f'{self.first} {self.last}'

    def introduce(self):
        return f'Hi, my name is {self.first} {self.last}, and I earn {self.pay} dollars per year.'


class Sqlbot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Sqlbot loaded')

    @commands.command()
    async def create(self, ctx, *, name):
        names = name.strip().split()
        emp1 = Employee(names[0], names[1], int(names[2]))
        insert_emp(emp1)
        await ctx.send(f'Added {names[0]} {names[1]} to database')

    @commands.command()
    async def search(self, ctx, *, last):
        emps = get_emps_by_name(last)
        await ctx.send(f'{emps}')

    @commands.command()
    async def update(self, ctx, *, info):
        infos = info.strip().split()
        update_pay(infos[0], int(infos[1]))
        await ctx.send("Set {}'s pay to {}".format(infos[0] , infos[1]))

    @commands.command()
    async def delete(self, ctx, *, first):
        remove_emp(first)
        await ctx.send(f'Deleted {first} from database')



def setup(client):
    client.add_cog(Sqlbot(client))
