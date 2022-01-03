from ..worker import TemporalWorker

class Workflow(TemporalWorker):
    
    name = "server_test"

    async def worker_workflow(self, payload: dict):
        return f"Hello, I'm gonna update some shit!....maybe"