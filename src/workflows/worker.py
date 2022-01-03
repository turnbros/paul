import logging
from util import config
from abc import ABC, abstractmethod
from temporal.workflow import workflow_method


logging.basicConfig(level=logging.DEBUG)


import functools
def example_workflow_method(queue_name):
	def decorator_repeat(func):
			@functools.wraps(func)
			def wrapper_example_workflow_method(*args, **kwargs):
					print(queue_name)
			return wrapper_example_workflow_method
	return decorator_repeat


class TemporalWorker(ABC):

	@property
	def paul_config(self):
		return config.Configuration()

	@property
	def temporal_config(self):
		return self.paul_config.read_temporal_config()

	@property
	def worker_config(self):
		return self.paul_config.read_workflow_config(self.name)

	@property
	@abstractmethod
	def name(self):
			raise NotImplementedError

	@abstractmethod
	async def worker_workflow(self, payload: dict):
		raise NotImplementedError

	async def execute(self, payload: dict):
		@workflow_method(task_queue=self.name)
		async def execute_workflow(self, payload: dict):
			return self.worker_workflow(payload)
		return execute_workflow(payload)
		





	
	
	
