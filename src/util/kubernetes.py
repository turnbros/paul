import os
import time
import asyncio
from kubernetes import client, config
from kubernetes.client.api.core_v1_api import CoreV1Api
from kubernetes.client import V1ConfigMap, V1ObjectMeta

class Cluster:
	def __init__(self):
		
		self.kubernetes_host = os.getenv("KUBERNETES_SERVICE_HOST", False)
		self.kubernetes_port = os.getenv("KUBERNETES_SERVICE_PORT", False)
		self.sa_mount_path = "/run/secrets/kubernetes.io/serviceaccount"
		self.namespace = "paul"
		self.configmap_name = "paul-cm"

		if self.kubernetes_host:
			with open(f"{self.sa_mount_path}/namespace") as namespace_file:
				self.namespace = namespace_file.read()

			with open(f"{self.sa_mount_path}/token") as token_file:	
				kube_config = client.Configuration()
				kube_config.api_key = {"authorization": f"Bearer {token_file.read()}"}
				kube_config.host =  f"https://{self.kubernetes_host}:{self.kubernetes_port}"
				kube_config.ssl_ca_cert = f"{self.sa_mount_path}/ca.crt"
				self._kube_api = client.CoreV1Api(client.ApiClient(kube_config))

		else:
			# This is NOT running inside K8s
			config.load_kube_config()
			self._kube_api = client.CoreV1Api()
	
	@property
	def api(self) -> CoreV1Api:
		return self._kube_api

	def read_config(self) -> V1ConfigMap:
		configmap: V1ConfigMap = self.api.read_namespaced_config_map(self.configmap_name, self.namespace)
		return configmap

	def watch_config(self, callback, interval: int = 3) -> V1ConfigMap:
		
		def get_configmap_version():
			configmap: V1ConfigMap = self.read_config
			configmap_metadata: V1ObjectMeta = configmap.metadata
			return configmap_metadata.resource_version

		async def version_check(callback, interval, initial_version):
			while(True):
				time.sleep(interval)
				if initial_version != get_configmap_version():
					callback(self.read_config())

		configmap: V1ConfigMap = self.read_config()
		configmap_version = get_configmap_version()
		asyncio.run(version_check(callback, interval, configmap_version))

		return configmap