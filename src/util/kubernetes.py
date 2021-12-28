import os
from kubernetes import client, config

configmap_name = os.getenv("CONFIGMAP_NAME")
k8s_endpoint = os.getenv("K8S_ENDPOINT")
sa_mount_path = os.getenv("SA_MOUNT_PATH")
configmap_name = os.getenv("CONFIGMAP_NAME")

class Cluster:
	def __init__(self, use_kubeconfig:bool = True):
		
		# Read the namespace this deployment is n
		with open(f"{sa_mount_path}/namespace") as namespace_file:
			self.namespace = namespace_file.read()

		# Configure the config or something
		if not use_kubeconfig:
			with open(f"{sa_mount_path}/token") as token_file:	
				kube_config = client.Configuration()
				kube_config.api_key["authorization"] = token_file.read()
				kube_config.api_key_prefix['authorization'] = 'Bearer'
				kube_config.host = k8s_endpoint
				kube_config.ssl_ca_cert = f"{sa_mount_path}/ca.crt"
				self.kube_api = client.CoreV1Api(client.ApiClient(kube_config))
		else:
			config.load_kube_config()
			self.kube_api = client.CoreV1Api()

		self.config = self.refresh_config
	
	def refresh_config(self) -> dict:
		configmap = self.kube_api.read_namespaced_config_map(configmap_name, self.namespace)
		return configmap.data
