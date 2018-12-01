import io
import os
import zipfile
from typing import Dict

from celery.result import AsyncResult
from flask import jsonify, send_file

from celery_app import c_app
from config import DATA_DIR
from database import get_celery_db
from log import get_logger
from tasks import get_images, get_text

logger = get_logger()


def fetch_images(body: Dict) -> Dict:
    url = body['url']
    task = get_images.delay(url)
    response = jsonify()
    response.headers['location'] = '/ml/content/images/{}'.format(task.id)
    response.status_code = 202
    return response


def fetch_text(body: Dict) -> Dict:
    url = body['url']
    task = get_text.delay(url)
    response = jsonify()
    response.headers['location'] = '/ml/content/text/{}'.format(task.id)
    response.status_code = 202
    return response


def _gen_image_fp():
    for file in os.listdir(DATA_DIR):
        yield os.path.join(DATA_DIR, file), file


def download_images():
    memory_bytes = io.BytesIO()
    with zipfile.ZipFile(memory_bytes, 'w') as z:
        for f_path, f_name in _gen_image_fp():
            z.write(f_path, f_name)
    memory_bytes.seek(0)
    return send_file(memory_bytes, as_attachment=True,
                     attachment_filename='ML_data_images.zip',
                     mimetype='application/zip')


def _gen_text_data(bytes_data: io.BytesIO) -> io.BytesIO:
    db = get_celery_db()
    text_cursor = db.text.find({'content': {'$exists': True}},
                               {'_id': 0, 'content': 1})
    for text in text_cursor:
        bytes_data.write(text["content"].encode('utf-8'))
    return bytes_data


def download_text():
    data = io.BytesIO()
    data = _gen_text_data(data).seek(0)
    return send_file(data, as_attachment=True,
                     attachment_filename='ML_data_text.txt',
                     mimetype='text/plain')


def download_all():
    zipped_data = io.BytesIO()
    with zipfile.ZipFile(zipped_data, 'w') as z:
        text_data = io.BytesIO()
        text_data = _gen_text_data(text_data)
        z.writestr('ML_data_text.txt', text_data.getvalue())
        for f_path, f_name in _gen_image_fp():
            z.write(f_path, f_name)
    zipped_data.seek(0)
    return send_file(zipped_data, as_attachment=True,
                     attachment_filename='ML_data_complete.zip',
                     mimetype='application/zip')


def _get_task_status(task_id: str) -> Dict:
    result = AsyncResult(task_id, app=c_app)
    state = result.state
    return {'state': state}


def get_image_task_status(task_id: str) -> Dict:
    return _get_task_status(task_id)


def get_text_task_status(task_id: str) -> Dict:
    return _get_task_status(task_id)
