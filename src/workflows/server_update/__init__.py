import asyncio
import logging
import os
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient


logging.basicConfig(level=logging.INFO)


TASK_QUEUE = "ServerUpdate"
NAMESPACE = "default"


# Workflow Implementation
class Workflow:
    @workflow_method(task_queue=TASK_QUEUE)
    async def execute(self, payload):
        return f"Howdy, {payload.get('name')}, I'm gonna update some shit!"


def get_temporal_ep():
    kubernetes_host = os.getenv("KUBERNETES_SERVICE_HOST", False)
    if kubernetes_host:
        return "temporal-frontend.temporal.svc.cluster.local", 7233
    else:
        return "localhost", 7233


async def worker_main():
    temporal_endpoint = get_temporal_ep()
    client = WorkflowClient.new_client(host=temporal_endpoint[0], port=temporal_endpoint[1], namespace=NAMESPACE)
    factory = WorkerFactory(client, NAMESPACE)
    worker = factory.new_worker(TASK_QUEUE)
    worker.register_workflow_implementation_type(Workflow)
    factory.start()
    print("Worker started")


async def start_worker():
    asyncio.ensure_future(worker_main())

    
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.ensure_future(worker_main())
    loop.run_forever()
    
    print("done")