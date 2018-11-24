import requests

from bs4 import BeautifulSoup
from bs4.element import Comment

from celery_app import c_app


def get_page(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def tag_visible(element):
    invisible_tags = ['style', 'script', 'head',
                      'title', 'meta', '[document]']
    if element.parent.name in invisible_tags:
        return False
    if isinstance(element, Comment):
        return False
    return True


@c_app.task
def get_images(url):
    page = get_page(url)
    images = page.select('img')
    # save images to MongoDB


@c_app.task
def get_text(url):
    page = get_page(url)
    texts = page.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    # " ".join(t.strip() for t in visible_texts)
