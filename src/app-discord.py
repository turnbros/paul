import os
import sys
import json
import discord
import logging
from http.client import HTTPSConnection, responses

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
        request_message = message.content.lower().replace(f"<@!{app_info.id}>", '')
        request_endpoint = os.getenv("DIALOGFLOW_ENDPOINT")
        request_path = os.getenv('DIALOGFLOW_PATH')
        request_headers = { 
            "Content-Type" : "application/json; charset=utf-8",
            "Authorization" : f"Bearer {os.getenv('DIALOGFLOW_TOKEN')}"
        }
        request_body = {
            "queryInput": {
                "text": {
                    "text": request_message,
                    "languageCode": "en"
                }
            },
            "queryParams": {
                "source": "DIALOGFLOW_CONSOLE",
                "timeZone": "America/Chicago",
                "sentimentAnalysisRequestConfig": {
                    "analyzeQueryTextSentiment": True
                }
            }
        }

        connection = HTTPSConnection(request_endpoint)
        connection.request('POST', request_path, headers=request_headers, body=json.dumps(request_body))
        response = connection.getresponse()
        
        if response.status == 200:
            response_data = response.read()
            response_json = json.loads(response_data)
            
            await message.channel.send(response_json["queryResult"]["fulfillmentText"])

        else:
            await message.channel.send("oh dear, something fucked up :-(")
            await message.channel.send("I blame @desidero for making me too complicated")


if __name__ == "__main__":
    discord_token = os.getenv("DISCORD_TOKEN", False)
    if discord_token:
        client.run(discord_token)