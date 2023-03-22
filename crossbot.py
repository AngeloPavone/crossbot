import generate
import regex as re

import discord


with open('token', 'r') as f:
    TOKEN = f.readlines()[0]


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

intents = discord.Intents.default()
intents.message_content = True
bot = MyClient(intents=intents)


async def send_crosshair(message) -> None:
        MATCH = re.search("^CSGO(-?[\\w]{5}){5}$", message.content)

        if MATCH:
            generate.SHARE_CODE = str(message.content)
            c = generate.Crosshair()
            generate.create_image(c)
            with open('crosshair.png', 'rb') as f:
                img = discord.File(f)
            await message.channel.send(file=img)
        else:
            await message.delete()


@bot.event
async def on_message(message):
    if message.channel.name == "bot-commands" or message.channel.name == "business":
        if message.author == bot.user:
            return
        await send_crosshair(message)
    else:
        return


bot.run(TOKEN)

def main():
    pass

if __name__ == "__main__":
    main()