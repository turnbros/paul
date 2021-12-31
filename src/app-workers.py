import os
import sys
import time
import asyncio
import logging
import importlib
import threading

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

if os.getenv("KUBERNETES_SERVICE_HOST", False):
    web_api_scheme = "http"
    web_api_host = "paul.paul.svc.cluster.local"
    web_api_port = 8443
else:
    web_api_scheme = "http"
    web_api_host = "localhost"
    web_api_port = 8443

def start_worker(name):
    logging.info(f"Starting worker {name}")
    imported_worker = importlib.import_module(f"workflows.{name}")
    worker_loop = asyncio.new_event_loop()
    worker_loop.create_task(imported_worker.worker_main())
    threading.Thread(name=f"{name}_worker", target=lambda: worker_loop.run_forever()).start()
    logging.info(f"Worker {name} started!")


if __name__ == "__main__":
    logging.info("Starting workers...")
    # TODO: make this dynamic
    workflows = [
        "server_count"
    ]
    for worker in workflows:
        start_worker(worker)
    logging.info("Workers started!")

    while(True):
        time.sleep(5)