import json
from .kubernetes import Cluster
from kubernetes.client import V1ConfigMap

class Configuration:
    def __init__(self) -> None:

        self.cluster = Cluster()
        self.config = self.cluster.read_config().data
        print(self.config)

    def read_workflow_config(self, name):
        workflows_configs = self.config.get("workflows")
        return json.loads(workflows_configs)