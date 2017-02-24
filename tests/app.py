from functools import partial

from sanic import Sanic
from sanic_graphql import GraphQLView
from graphql.execution.executors.asyncio import AsyncioExecutor

from .schema import Schema


def create_app(path='/graphql', **kwargs):
    app = Sanic(__name__)
    app.debug = True

    schema = kwargs.pop('schema', None) or Schema
    async_executor = kwargs.pop('async_executor', False)

    if async_executor:
        def init_async_executor(app, loop):
            executor = AsyncioExecutor(loop)
            app.add_route(GraphQLView.as_view(schema=schema, executor=executor, **kwargs), path)

        def remove_graphql_endpoint(app, loop):
            app.remove_route(path)

        app.server_kwargs = dict(
            before_start=init_async_executor,
            after_stop=remove_graphql_endpoint
        )
    else:
        app.add_route(GraphQLView.as_view(schema=schema, **kwargs), path)
        app.server_kwargs = dict()

    return app

