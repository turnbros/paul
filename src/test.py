import asyncio
import logging
import workflows

logging.basicConfig(level=logging.INFO)

# workflow_catalog = workflows.WorkflowCatalog()
# def register_workflow(workflow_name):
#     logging.debug(f"Register workflow {workflow_name}")
#     if workflow_catalog.register_workflow(workflow_name):
#         logging.info(f"Workflow {workflow_name} registered")
#     else:
#         logging.error(f"Failed to register {workflow_name}")

from util import config
if __name__ == "__main__":
    configs = config.Configuration()
    print(configs.read_temporal_config())
    print(configs.read_dialogflow_config())
    print(configs.read_discord_config())
    print(configs.read_workflow_config("server_count"))


# if __name__ == "__main__":
#     workflows = [
#         "server_count"
#     ]
#     for workflow in workflows:
#         workflow_catalog.register_workflow(workflow)
#     asyncio.run(workflow_catalog.execute_workflow("server_count"))


# if __name__ == "__main__":
#   paul_dialog = PaulDialog(
#       project_id = 'paul-fmma',
#       language_code = "en"
#     )
#   session_id = paul_dialog.create_session()
#   asdf = paul_dialog.handle_input(session_id, "hello!")
# 
#   qwer = asdf.query_result.fulfillment_text
# 
# 
#   print(type(qwer))