from celery import Celery
from utils.dd_utils import run_dd_clone
import json
import time

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task(bind=True)
def clone_disk(self, source, destination):
    start = time.time()
    result = run_dd_clone(source, destination)
    end = time.time()

    # Save to history
    with open("logs/history.json", 'r+') as f:
        history = json.load(f)
        history.insert(0, {
            'source': source,
            'destination': destination,
            'duration': round(end - start, 2),
            'status': result['status']
        })
        f.seek(0)
        json.dump(history[:10], f, indent=2)

    return result

def get_status(task_id):
    async_result = clone_disk.AsyncResult(task_id)
    return {'status': async_result.status, 'result': async_result.result}

