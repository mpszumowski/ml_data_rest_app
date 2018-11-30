import os
from urllib.parse import urljoin
from urllib.request import urlretrieve

import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from bson.objectid import ObjectId

from celery_app import c_app
from config import DATA_DIR
from database import get_celery_db

db = get_celery_db()


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
    db.text.insert_one({'task_id': self.request.id,
                        'url': url,
                        'content': text})
    return True


@c_app.task(bind=True)
def get_images(self, url):
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
