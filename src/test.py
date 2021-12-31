import asyncio
import logging
import workflows

logging.basicConfig(level=logging.INFO)

workflow_catalog = workflows.WorkflowCatalog()
def register_workflow(workflow_name):
    logging.debug(f"Register workflow {workflow_name}")
    if workflow_catalog.register_workflow(workflow_name):
        logging.info(f"Workflow {workflow_name} registered")
    else:
        logging.error(f"Failed to register {workflow_name}")

if __name__ == "__main__":
    workflows = [
        "server_count"
    ]
    for workflow in workflows:
        register_workflow(workflow)


    asyncio.run(workflow_catalog.execute_workflow("server_count"))