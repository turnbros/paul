import os
import sys
import json
import asyncio
import logging
import importlib
import threading
from util import kubernetes
from http.client import HTTPSConnection, HTTPConnection


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


if os.getenv("KUBERNETES_SERVICE_HOST", False):
    web_api_scheme = "https"
    web_api_host = "paul-web-api.paul.svc.cluster.local"
    web_api_port = 8443
else:
    web_api_scheme = "http"
    web_api_host = "localhost"
    web_api_port = 8443


def register_worker(name):
    logging.info(f"register worker {name}")
    if web_api_scheme == "https":
        connection = HTTPSConnection(host=web_api_host, port=web_api_port)
    else:
        connection = HTTPConnection(host=web_api_host, port=web_api_port)

    connection.request('PUT', "/api/v1/workflow", body=json.dumps({
        "name": name
    }))
    response = connection.getresponse()
    if response.status == 204:
        logging.info(f"{name} registered!")
        return True
    else:
        logging.info(f"Failed to register {name}")
        return False


def start_worker(name):
    logging.info(f"Starting worker {name}")
    imported_worker = importlib.import_module(f"workflows.{name}")
    worker_loop = asyncio.new_event_loop()
    worker_loop.create_task(imported_worker.worker_main())
    threading.Thread(name=f"{name}_worker", target=lambda: worker_loop.run_forever()).start()
    logging.info(f"Worker {name} started!")


if __name__ == "__main__":
    logging.info("Starting worker registration...")
    k8s_client = kubernetes.Cluster()
    config = k8s_client.read_configmap()
    routes = config["intent_workflow_routes"]
    logging.info("Registering workers...")
    for worker in routes.values():
        if register_worker(worker):
            start_worker(worker)
    logging.info("Worker registration complete")

    while(True):
        pass