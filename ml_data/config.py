import os

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

celery_cfg = {
    'broker': os.environ.get('CELERY_BROKER'),
    'backend': os.environ.get('CELERY_BACKEND')
}

rest_cfg = {
    'address': os.environ.get('APP_ADDRESS'),
    'port': os.environ.get('PORT')
}
