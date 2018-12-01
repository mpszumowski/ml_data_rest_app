from unittest import mock

from ml_data import api, serve


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
def test_download_images(mock__gen_image_fp):
    with serve.app.test_request_context('/ml/content/images'):
        response = api.download_images()
    assert response.mimetype == 'application/zip'
    assert response.status_code == 200


@mock.patch('ml_data.api._gen_text_data')
def test_download_text(mock__gen_text_data):
    with serve.app.test_request_context('/ml/content/text'):
        response = api.download_text()
    assert response.mimetype == 'text/plain'
    assert response.status_code == 200


@mock.patch('ml_data.api._gen_text_data')
@mock.patch('ml_data.api._gen_image_fp')
def test_download_all(mock__gen_image_fp, mock__gen_text_data):
    mock__gen_text_data().getvalue.return_value = b'image'
    mock__gen_image_fp.result_value = b'f_path', b'f_name'
    with serve.app.test_request_context('/ml/content'):
        response = api.download_all()
    assert response.mimetype == 'application/zip'
    assert response.status_code == 200


def test_get_status():
    api.c_app.conf.task_always_eager = True

