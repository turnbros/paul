import json
from typing import Union
from .kubernetes import Cluster

class Configuration:
    def __init__(self) -> None:
        self.cluster = Cluster()
        self.config = self.cluster.read_config().data
        print(self.config)

    def read_temporal_config(self) -> dict:
        return json.loads(self.config.get("temporal"))

    def read_dialogflow_config(self) -> dict:
        return json.loads(self.config.get("dialogflow"))

    def read_discord_config(self) -> dict:
        return json.loads(self.config.get("discord"))

    def read_workflow_config(self, name) -> Union[dict, None]:
        workflow_configs = json.loads(self.config.get("workflows"))
        for workflow_config in workflow_configs:
            if workflow_config.get("name") == name:
                return workflow_config
        return None