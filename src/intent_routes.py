import asyncio
import importlib.util
from temporal.workflow import workflow_method, WorkflowClient
import importlib


NAMESPACE = "default"


registered_intents = {}
def register_intent_workflow(workflow_name):
    registered_intents[workflow_name] = importlib.import_module(f"workflows.{workflow_name}")


async def execute_intent_workflow(intent_workflow, **kwargs):
    print(f"execute_intent_workflow: {intent_workflow}")

    client = WorkflowClient.new_client(namespace=NAMESPACE)
    registered_workflow: registered_intents[intent_workflow].WorkflowStub = client.new_workflow_stub(registered_intents[intent_workflow].WorkflowStub)
    result = await registered_workflow.execute(kwargs)
    return result


if __name__ == '__main__':    
    register_intent_workflow("server_count")
    register_intent_workflow("server_update")

    response = asyncio.run(execute_intent_workflow("server_count", name="bob", count=42))
    print(response)

    response = asyncio.run(execute_intent_workflow("server_update", name="bob"))
    print(response)