from typing import Dict

from celery.result import AsyncResult

import tasks
from celery_app import c_app
from log import get_logger

logger = get_logger()


def download_images(body: Dict) -> Dict:
    url = body['url']
    task = tasks.get_images.delay(url)
    return {'task_id': task.id}


def download_text(body: Dict) -> Dict:
    url = body['url']
    task = tasks.get_text.delay(url)
    return {'task_id': task.id}


def fetch_images():
    pass


def fetch_text():
    pass


def fetch_all():
    pass


def check_task(task_id: str) -> Dict:
    result = AsyncResult(task_id, app=c_app)
    state = result.state
    return {'state': state}
