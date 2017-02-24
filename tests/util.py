import pytest

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from sanic.utils import sanic_endpoint_test

from .app import create_app


@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client():
    class Client:
        def get(self, app, uri, **kwargs):
            kwargs['method'] = 'get'
            return sanic_endpoint_test(app, uri=uri, gather_request=False,
                                       server_kwargs=app.server_kwargs, **kwargs)

        def post(self, app, uri, **kwargs):
            kwargs['method'] = 'post'
            return sanic_endpoint_test(app, uri=uri, gather_request=False,
                                       server_kwargs=app.server_kwargs, **kwargs)

        def put(self, app, uri, **kwargs):
            kwargs['method'] = 'put'
            return sanic_endpoint_test(app, uri=uri, gather_request=False,
                                       server_kwargs=app.server_kwargs, **kwargs)

    return Client()

def url_string(uri='/graphql', **url_params):
    string = '/graphql'

    if url_params:
        string += '?' + urlencode(url_params)

    return string
