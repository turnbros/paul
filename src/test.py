from os import stat
from workflows.worker import TemporalWorker
import asyncio

class TestTemporalWorker(TemporalWorker):
    
    name = "test_temporal_worker"

    async def worker_workflow(self, payload: dict):
        return f"Hello, I'm gonna update some shit!"

    
    

if __name__ == "__main__":
    print("starting")
    test_temporal_worker = TestTemporalWorker()
    TestTemporalWorker().
    asyncio.run(test_temporal_worker.execute({}))
    print("done")