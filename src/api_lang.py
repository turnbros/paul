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

    app_info = await client.application_info()

    if message.content.startswith(f"<@!{app_info.id}>"):
        if "how are you" in message.content.lower():
            await message.channel.send("I'm fine, thank you for asking!")

client.run(os.getenv("DISCORD_TOKEN"))