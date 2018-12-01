import pytest
from unittest import mock

from ml_data import *


@mock.patch('ml_data.api.get_images')
def test_fetch_images(mock_get_images):
    request_body = {'url': 'http://www.another.url'}
    with serve.app.app_context():
        response = api.fetch_images(request_body)
    assert response.status_code == 202
    assert response.headers['location'].split('/')[-1] is not None


@mock.patch('ml_data.api.get_text')
def test_fetch_text(mock_get_text):
    request_body = {'url': 'http://www.another.url'}
    with serve.app.app_context():
        response = api.fetch_text(request_body)
    assert response.status_code == 202
    assert response.headers['location'].split('/')[-1] is not None


@mock.patch('ml_data.api._gen_image_fp')
def test_download_images(_gen_image_fp):
    pass


def test_download_text():
    pass


def test_download_all():
    pass
