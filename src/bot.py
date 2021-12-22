import os
import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'I have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    message.content.
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    else:
        await message.channel.send('I dont understand')

client.run(os.getenv("DISCORD_TOKEN"))