import os
import sys
import asyncio
import logging
from util import kubernetes
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient

logging.basicConfig(level=logging.INFO)

kube = kubernetes.Cluster()

TASK_QUEUE = "ServerCount"
NAMESPACE = "default"


def count_running_servers(filters: dict = None):
    return len(kube.count_game_servers())



class Workflow:
    @workflow_method(task_queue=TASK_QUEUE)
    async def execute(self, payload: dict):
        
        game_type = payload.get("gametype", False)
        server_count = count_running_servers()

        if game_type:
            if server_count > 0:
                return f"I found {server_count} running {game_type} servers"
            return f"Unfortunately I couldn't find any {game_type} servers..."

        if server_count > 0:
            return f"Sure thing! There are {server_count} running servers in total"
        return "Something may have gone wrong because I didn't find any servers..."





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