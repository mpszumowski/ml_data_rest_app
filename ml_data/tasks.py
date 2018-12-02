import os
from urllib.parse import urljoin
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from bson.objectid import ObjectId
from pymongo import MongoClient

from ml_data.celery_app import c_app
from ml_data.config import DATA_DIR
from ml_data.database import MongoCfg


def get_page(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def tag_visible(element):
    invisible_tags = ['style', 'script', 'head',
                      'title', 'meta', '[document]']
    if isinstance(element, Comment) or element.parent.name in invisible_tags:
        return False
    return True


@c_app.task(bind=True)
def get_text(self, url):
    page = get_page(url)
    texts = page.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    text = ' '.join(t.strip() for t in visible_texts)
    db = MongoClient(**MongoCfg.client)[MongoCfg.db_name]
    db.text.insert_one({'task_id': self.request.id,
                        'url': url,
                        'content': text})
    return True


@c_app.task(bind=True)
def get_images(self, url):
    db = MongoClient(**MongoCfg.client)[MongoCfg.db_name]
    logger = c_app.log.get_default_logger()
    logger.info(os.getuid())
    page = get_page(url)
    for img_tag in page.find_all('img'):
        img_url = urljoin(url, img_tag['src'])
        img_name = img_url.split('/')[-1]
        object_id = ObjectId()
        filename = '{}_{}'.format(object_id, img_name)
        urlretrieve(img_url, os.path.join(DATA_DIR, filename))
        db.images.insert_one({'_id': object_id,
                              'task_id': self.request.id,
                              'url': url,
                              'filename': filename})
    return True
