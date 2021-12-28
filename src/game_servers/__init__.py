from abc import abstractmethod, abstractproperty


class GameServer:

	@abstractproperty
	def version(self):
		pass

	@abstractmethod
	def update_available(self):
		pass


class SteamGameServer(GameServer):
	
	def __init__(self, server_endpoint) -> None:
		self.server_endpoint = server_endpoint

	@abstractproperty
	def app_id(self):
		pass

	def version(self):
		pass
	
	def update_available(self):
		pass