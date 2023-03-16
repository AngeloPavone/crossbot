import os
import generate

import discord
from discord.ext import commands


with open('token', 'r') as f:
    TOKEN = f.readlines()[0]


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

intents = discord.Intents.default()
intents.message_content = True
bot = MyClient(intents=intents)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('CSGO'):
        generate.SHARE_CODE = str(message.content)
        c = generate.Crosshair()
        generate.create_image()
        with open('crosshair.png', 'rb') as f:
            img = discord.File(f)
        await message.channel.send(file=img)
        await message.channel.send(c.get_crosshair_settings())


bot.run(TOKEN)

def main():
    pass

if __name__ == "__main__":
    main()