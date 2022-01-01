import os
import logging
from util import kubernetes
from util import config
from temporal.workerfactory import WorkerFactory
from temporal.workflow import workflow_method, Workflow, WorkflowClient


logging.basicConfig(level=logging.INFO)


kube = kubernetes.Cluster()
paul_config = config.Configuration()
worker_config = paul_config.read_workflow_config("server_count")
temporal_config = paul_config.read_temporal_config()


TASK_QUEUE = worker_config.get("task_queue")
if TASK_QUEUE is None:
    raise Exception("Missing worker task_queue configuration!")


NAMESPACE = temporal_config.get("namespace")
if NAMESPACE is None:
    raise Exception("Missing temporal namespace configuration!")


def count_running_servers(game_type: str = None):
    if game_type is None:
        server_list = kube.api.list_pod_for_all_namespaces(label_selector=f"gaming.turnbros.app/role=server")
    else:
        server_list = kube.api.list_pod_for_all_namespaces(label_selector=f"gaming.turnbros.app/type={game_type}")
    return len(server_list.items)
    

class Workflow:
    @workflow_method(task_queue=TASK_QUEUE)
    async def execute(self, payload: dict):
        
        game_type = payload.get("gametype")
        server_count = count_running_servers(game_type)

        if game_type is not None:
            if server_count > 0:
                return f"I found {server_count} running {game_type} servers"
            return f"Unfortunately I couldn't find any {game_type} servers..."

        if server_count > 0:
            return f"Sure thing! There are {server_count} running servers in total"
        return "Something may have gone wrong because I didn't find any servers..."


async def worker_main():
    # Simple check to see if we're outside k8s
    if os.getenv("KUBERNETES_SERVICE_HOST", False):
        temporal_host = temporal_config.get("host")
    else:
        temporal_host = "localhost"    

    temporal_port = temporal_config.get("port")

    client = WorkflowClient.new_client(host=temporal_host, port=temporal_port, namespace=NAMESPACE)
    factory = WorkerFactory(client, NAMESPACE)
    worker = factory.new_worker(TASK_QUEUE)
    worker.register_workflow_implementation_type(Workflow)
    factory.start()
    logging.info("Worker started")