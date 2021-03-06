import os
import logging
import traceback
import importlib
import importlib.util
from typing import Any
from temporal.workflow import WorkflowClient


logging.basicConfig(level=logging.INFO)


class Workflow(object):
    def __init__(self, name, module):
        self._name = name
        self._module = module

    @property
    def name(self):
        return self._name

    @property
    def module(self):
        return self._module

    def get_stub(self) -> Any:
        return self.module.WorkflowStub


class WorkflowCatalog(object):

    def __init__(self):
        self._workflows = {}
        self.namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

        if os.getenv("KUBERNETES_SERVICE_HOST", False):
            self.temporal_host = "temporal-frontend.temporal.svc.cluster.local"
            self.temporal_port = 7233
        else:
            self.temporal_host = "localhost"
            self.temporal_port = 7233


    @property
    def workflows(self):
        return self._workflows


    def get_workflow(self, name: str) -> Workflow:
        return self._workflows[name]


    # TODO: See if there's maybe a way to include the workflow parameter schema
    def register_workflow(self, name: str):
        logging.info(f"Registering workflow: {name}...")
        try:
            self._workflows[name] = Workflow(name, importlib.import_module(f"workflows.{name}"))
            logging.info(f"Registration complete: {name}")
            return True
        except Exception as error:
            traceback.print_exc()
            logging.error(f"Registration of {name} failed with error {error}")
        return False


    async def execute_workflow(self, name, payload: dict):
        logging.info(f"Executing workflow: {name}")

        workflow = self.get_workflow(name)
        if workflow is None:
            raise Exception(f"Workflow {name} not found!")

        try:
            client = WorkflowClient.new_client(host=self.temporal_host,
                                                port=self.temporal_port,
                                                namespace=self.namespace)
            workflow = importlib.import_module(f"workflows.{name}")
            registered_workflow: workflow.Workflow = client.new_workflow_stub(workflow.Workflow)
            result = await registered_workflow.execute(payload)

        except Exception as error:
            traceback.print_exc()
            logging.error(f"Execution of {name} failed with error {error}")
            result = None

        return result