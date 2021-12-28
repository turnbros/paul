import asyncio
import logging
from datetime import timedelta

from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient


logging.basicConfig(level=logging.INFO)


TASK_QUEUE = "ServerCount"
NAMESPACE = "default"


# Workflow Interface
class WorkflowStub:
    @workflow_method(task_queue=TASK_QUEUE)
    async def execute(self, payload: dict):
        raise NotImplementedError


# Workflow Implementation
class Workflow(WorkflowStub):
    async def execute(self, payload: dict):
        return f"Howdy, {payload.get('name')}, the answer is {payload.get('count')}!"


async def worker_main():
    client = WorkflowClient.new_client(namespace=NAMESPACE)
    factory = WorkerFactory(client, NAMESPACE)
    worker = factory.new_worker(TASK_QUEUE)
    worker.register_workflow_implementation_type(Workflow)
    factory.start()
    print("Worker started")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(worker_main())
    loop.run_forever()

