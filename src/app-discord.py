import os
import sys
import discord
import logging
import workflows
import traceback
from dialogflow import PaulDialog
from util import config


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


client = discord.Client()
paul_config = config.Configuration()
paul_dialog = PaulDialog(
    project_id = paul_config.read_dialogflow_config().get('project_id'),
    language_code = paul_config.read_dialogflow_config().get('language_code')
)


workflow_catalog = workflows.WorkflowCatalog()
enabled_workflows = []
for workflow_config in paul_config.read_workflow_config():
    enabled_workflows.append(workflow_config.get("name"))


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
            intent_name = response.query_result.intent.display_name
            intent_parameters = response.query_result.parameters

            parameters = {}
            for parameter in intent_parameters.items():
                parameters[parameter[0]] = parameter[1]

            if intent_name in enabled_workflows:
                response_message = await workflow_catalog.execute_workflow(intent_name, parameters)
            else:
                response_message = response.query_result.fulfillment_text
            
            await message.channel.send(response_message)

        except Exception as error:
            traceback.print_exc()
            logging.error(error)
            await message.channel.send("oh dear, something fucked up :-(")
            await message.channel.send("kill meeeeeee")


if __name__ == "__main__":
    for workflow in enabled_workflows:
        workflow_catalog.register_workflow(workflow)
    discord_token = os.getenv("DISCORD_TOKEN", False)
    if discord_token:
        client.run(discord_token)