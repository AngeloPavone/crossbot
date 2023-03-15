import os

import discord
from discord.ext import commands

with open('token', 'r') as f:
    TOKEN = f.readlines()[0]


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(TOKEN)

def main():
    print(f'Hello, World!')
    pass

if __name__ == "__main__":
    main()