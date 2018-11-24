from typing import Dict

import tasks


def download_images(url: str) -> Dict:
    task_id = tasks.get_images.apply_async(args=[url])
    return {'task_id': task_id}


def download_text(url: str) -> Dict:
    task_id = tasks.get_text.apply_async(args=[url])
    return {'task_id': task_id}


def fetch_images():
    pass


def fetch_text():
    pass


def fetch_all():
    pass


def check_task(task_id: str) -> Dict:
    pass
