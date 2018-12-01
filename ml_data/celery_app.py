from celery import Celery, exceptions

from ml_data.config import celery_cfg


def create_celery_app():
    app_name = 'ml_data.celery_app'
    include = ['ml_data.tasks']
    try:
        app = Celery(app_name=app_name,
                     broker=celery_cfg['broker'],
                     backend=celery_cfg['broker'],
                     include=include)
    except exceptions.CeleryError as e:
        raise e
    return app


c_app = create_celery_app()
