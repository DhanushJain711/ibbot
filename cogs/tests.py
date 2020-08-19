import discord
import random
from discord.ext import commands

class Tests(commands.Cog):

    def __init__(self,client):
        self.client = client

    #events

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tests loaded')

    @commands.Cog.listener()
    async def on_command_error(self, ctx,error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('This is an invalid command. Type "!help" for list of commands.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter necessary parameters')

    @commands.command()
    async def hello(self, ctx, *, name):
        if (name == 'hardik'):
            await ctx.send(f'Happy birthday {name}')
        else:
            await ctx.send(f'Fuck you {name}')

    @commands.command(aliases = ['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def addall(self, ctx, *, nums):

        numbers = list(map(int, nums.strip().split()))
        result = 0
        question = ' '

        for i in numbers:
            result += i

        for i in range(len(numbers)):
            question += str(numbers[i])
            if i == len(numbers) - 1 :
                question += '='
            else:
                question += '+'

        await ctx.send(f'{question}{result}')

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def user(self, ctx):
        author = str(ctx.author)
        await ctx.send(f'Hi, {author[:-5]}, with code {author[-4:]}')

    @commands.group(invoke_without_command = True)
    async def calc(self, ctx):
        await ctx.send('Add, substract, multiply, or divide')

    @calc.command()
    async def add(self, ctx, *, nums):
        numbers = list(map(int, nums.strip().split()))
        result = numbers[0] + numbers[1]
        await ctx.send(result)

    @calc.command()
    async def sub(self, ctx, *, nums):
        numbers = list(map(int, nums.strip().split()))
        result = numbers[0] - numbers[1]
        await ctx.send(result)

    @calc.command()
    async def mult(self, ctx, *, nums):
        numbers = list(map(int, nums.strip().split()))
        result = numbers[0] * numbers[1]
        await ctx.send(result)

    @calc.command()
    async def div(self, ctx, *, nums):
        numbers = list(map(int, nums.strip().split()))
        result = numbers[0] / numbers[1]
        await ctx.send(result)




def setup(client):
    client.add_cog(Tests(client))
