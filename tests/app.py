import pytest

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from sanic import Sanic
from sanic.testing import SanicTestClient
from sanic_graphql import GraphQLView
from graphql.execution.executors.asyncio import AsyncioExecutor

from .schema import Schema


def create_app(path='/graphql', **kwargs):
    app = Sanic(__name__)
    app.debug = True

    schema = kwargs.pop('schema', None) or Schema
    async_executor = kwargs.pop('async_executor', False)

    if async_executor:
        @app.listener('before_server_start')
        def init_async_executor(app, loop):
            executor = AsyncioExecutor(loop)
            app.add_route(GraphQLView.as_view(schema=schema, executor=executor, **kwargs), path)

        @app.listener('before_server_stop')
        def remove_graphql_endpoint(app, loop):
            app.remove_route(path)
    else:
        app.add_route(GraphQLView.as_view(schema=schema, **kwargs), path)

    app.client = SanicTestClient(app)
    return app


def url_string(uri='/graphql', **url_params):
    string = '/graphql'

    if url_params:
        string += '?' + urlencode(url_params)

    return string


def parametrize_sync_async_app_test(arg, **extra_options):
    def decorator(test):
        apps = []
        for ae in [False, True]:
            apps.append(create_app(async_executor=ae, **extra_options))

        return pytest.mark.parametrize('app', apps)(test)
    return decorator
