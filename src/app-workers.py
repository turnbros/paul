import sys
import time
import asyncio
import logging
import importlib
import threading


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


def start_worker(name):
    logging.info(f"Starting worker {name}")
    imported_worker = importlib.import_module(f"workflows.{name}")
    worker_loop = asyncio.new_event_loop()
    worker_loop.create_task(imported_worker.worker_main())
    threading.Thread(name=f"{name}_worker", target=lambda: worker_loop.run_forever()).start()
    logging.info(f"Worker {name} started!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_worker(sys.argv[1])
        while(True):
            time.sleep(5)