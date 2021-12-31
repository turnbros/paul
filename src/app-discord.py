import os
import sys
import discord
import logging
from src.dialogflow import PaulDialog

paul_dialog = PaulDialog(
      key_path = os.getenv('DIALOGFLOW_CRED_PATH'),
      project_id = os.getenv('DIALOGFLOW_PROJECT_ID'),
      language_code = os.getenv("DIALOGFLOW_LANG_CODE")
    )

client = discord.Client()
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

@client.event
async def on_ready():
    logging.info(f'I have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    app_info = await client.application_info()
    logging.info(message)

    if message.content.startswith(f"<@!{app_info.id}>"):
        try:
            request_message = message.content.lower().replace(f"<@!{app_info.id}>", '')
            session_id = paul_dialog.create_session()
            response = paul_dialog.handle_input(session_id, request_message)
            await message.channel.send(response["queryResult"]["fulfillmentText"])

        except Exception as error:
            logging.error(error)
            await message.channel.send("oh dear, something fucked up :-(")
            await message.channel.send("I blame @desidero for making me too complicated")


if __name__ == "__main__":
    discord_token = os.getenv("DISCORD_TOKEN", False)
    if discord_token:
        client.run(discord_token)