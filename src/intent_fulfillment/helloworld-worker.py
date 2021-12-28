

import asyncio
import logging
from datetime import timedelta

from temporal.activity_method import activity_method
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient

logging.basicConfig(level=logging.INFO)

TASK_QUEUE = "HelloWorld"
NAMESPACE = "default"


# Activities Interface
class GreetingActivities:
    @activity_method(task_queue=TASK_QUEUE, schedule_to_close_timeout=timedelta(seconds=60))
    async def compose_greeting(self, greeting: str, name: str) -> str:
        raise NotImplementedError


# Activities Implementation
class GreetingActivitiesImpl:
    async def compose_greeting(self, greeting: str, name: str) -> str:
        return greeting + " " + name


# Workflow Interface
class GreetingWorkflow:
    @workflow_method(task_queue=TASK_QUEUE)
    async def get_greeting(self, name: str) -> str:
        raise NotImplementedError


# Workflow Implementation
class GreetingWorkflowImpl(GreetingWorkflow):

    def __init__(self):
        self.greeting_activities: GreetingActivities = Workflow.new_activity_stub(GreetingActivities)

    async def get_greeting(self, name):
        return await self.greeting_activities.compose_greeting("Hello!", name)


async def worker_main():
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    factory = WorkerFactory(client, NAMESPACE)
    worker = factory.new_worker(TASK_QUEUE)
    worker.register_activities_implementation(GreetingActivitiesImpl(), "GreetingActivities")
    worker.register_workflow_implementation_type(GreetingWorkflowImpl)
    factory.start()
    print("Worker started")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  # (1)
    asyncio.ensure_future(worker_main())
    loop.run_forever()

