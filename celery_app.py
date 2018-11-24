import os

from celery import Celery, exceptions


def create_celery_app():
    app_name = 'celery_app'
    broker = os.environ.get('CELERY_BROKER')
    backend = os.environ.get('CELERY_BACKEND')
    include = ['tasks']
    try:
        app = Celery(app_name=app_name, broker=broker,
                     backend=backend, include=include)
        return app
    except exceptions.CeleryError as e:
        raise e


c_app = create_celery_app()
