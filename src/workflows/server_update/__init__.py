import logging
from workflows.worker import TemporalWorker


logging.basicConfig(level=logging.INFO)


class Workflow(TemporalWorker):
    
    name = "server_test"

    async def worker_workflow(self, payload: dict):
        logging.info("Log from worker_workflow")
        return f"Hello, I'm gonna update some shit!....maybe"

#import os
#import logging
#from util import kubernetes
#from util import config
#from temporal.workerfactory import WorkerFactory
#from temporal.workflow import workflow_method, Workflow, WorkflowClient
#
#
#logging.basicConfig(level=logging.INFO)
#
#
#kube = kubernetes.Cluster()
#paul_config = config.Configuration()
#worker_config = paul_config.read_workflow_config("server_update")
#temporal_config = paul_config.read_temporal_config()
#
#
#TASK_QUEUE = worker_config.get("task_queue")
#if TASK_QUEUE is None:
#    raise Exception("Missing worker task_queue configuration!")
#
#
#NAMESPACE = temporal_config.get("namespace")
#if NAMESPACE is None:
#    raise Exception("Missing temporal namespace configuration!")
#
#
## Workflow Implementation
#class Workflow:
#    @workflow_method(task_queue=TASK_QUEUE)
#    async def execute(self, payload: dict):
#        return f"Howdy, {payload.get('name')}, I'm gonna update some shit!"
#
#
#async def worker_main():
#    # Simple check to see if we're outside k8s
#    if os.getenv("KUBERNETES_SERVICE_HOST", False):
#        temporal_host = temporal_config.get("host")
#    else:
#        temporal_host = "localhost"    
#
#    temporal_port = temporal_config.get("port")
#
#    client = WorkflowClient.new_client(host=temporal_host, port=temporal_port, namespace=NAMESPACE)
#    factory = WorkerFactory(client, NAMESPACE)
#    worker = factory.new_worker(TASK_QUEUE)
#    worker.register_workflow_implementation_type(Workflow)
#    factory.start()
#    logging.info("Worker started")