import os
import sys
import discord
import logging
import workflows
import traceback
from dialogflow import PaulDialog


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


client = discord.Client()
paul_dialog = PaulDialog(
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID'),
    language_code = os.getenv("DIALOGFLOW_LANG_CODE")
)


# TODO: Make this dynamic (maybe via helm?)
workflow_catalog = workflows.WorkflowCatalog()
enabled_workflows = [
    "server_count"
]


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

            session_id = paul_dialog.create_session()
            paul_dialog.handle_input(session_id, "hello!")
            print(response)

            response_intent = response.query_result.intent.display_name
            response_message = response.query_result.fulfillment_text

            if response_intent in enabled_workflows:
                response_message = await workflow_catalog.execute_workflow(response_intent)

            await message.channel.send(response_message)

        except Exception as error:
            traceback.print_exc()
            logging.error(error)
            await message.channel.send("oh dear, something fucked up :-(")
            await message.channel.send("I blame @desidero for making me too complicated")


if __name__ == "__main__":
    for workflow in enabled_workflows:
        workflow_catalog.register_workflow(workflow)
    discord_token = os.getenv("DISCORD_TOKEN", False)
    if discord_token:
        client.run(discord_token)