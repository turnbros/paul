import os
import sys
import asyncio
import logging
import importlib
from util import config
from temporal.workflow import WorkflowClient
from temporal.workerfactory import WorkerFactory


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


async def start_worker(name):
	logging.info(f"Starting worker {name}")
	paul_config = config.Configuration()
	worker_config = paul_config.read_workflow_config("server_update")
	temporal_config = paul_config.read_temporal_config()

	# Simple check to see if we're outside k8s
	if os.getenv("KUBERNETES_SERVICE_HOST", False):
		temporal_host = temporal_config.get("host")
	else:
		temporal_host = "localhost"    
	temporal_port = temporal_config.get("port")

	task_queue = worker_config.get("task_queue")
	if task_queue is None:
		raise Exception("Missing worker task_queue configuration!")

	namespace = temporal_config.get("namespace")
	if namespace is None:
		raise Exception("Missing temporal namespace configuration!")

	imported_worker = importlib.import_module(f"workflows.{name}")
	client = WorkflowClient.new_client(host=temporal_host, port=temporal_port, namespace=namespace)
	factory = WorkerFactory(client, namespace)
	worker = factory.new_worker(task_queue)
	worker.register_workflow_implementation_type(imported_worker.Workflow)	
	factory.start()
	logging.info("Worker started")


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("too many args!")
		exit()

	worker_loop = asyncio.new_event_loop()
	worker_loop.create_task(start_worker(sys.argv[1]))
	worker_loop.run_forever()