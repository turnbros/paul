import os
from kubernetes import client, config
import kubernetes
from kubernetes.client.api.core_v1_api import CoreV1Api

configmap_name = os.getenv("CONFIGMAP_NAME")
k8s_endpoint = os.getenv("K8S_ENDPOINT")
sa_mount_path = os.getenv("SA_MOUNT_PATH")
configmap_name = os.getenv("CONFIGMAP_NAME")

class Cluster:
	def __init__(self, use_kubeconfig:bool = True):
		
		self.namespace = os.getenv("K8S_NAMESPACE")
		if self.namespace is None:
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
			self._kube_api = client.CoreV1Api()

		self.config = self.refresh_config
	
	@property
	def api(self) -> CoreV1Api:
		return self._kube_api

	def refresh_config(self) -> dict:
		configmap = self.api.list_pod_for_all_namespaces()
		return configmap.data

	
	def client(self):
		pass



	def count_game_servers(self):
		pod_list = self.api.list_pod_for_all_namespaces()
		print(pod_list)
		return pod_list.items