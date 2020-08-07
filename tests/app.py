from urllib.parse import urlencode

from sanic import Sanic
from sanic.testing import SanicTestClient

from sanic_graphql import GraphQLView

from .schema import Schema


def create_app(path="/graphql", **kwargs):
    app = Sanic(__name__)
    app.debug = True

    schema = kwargs.pop("schema", None) or Schema
    app.add_route(GraphQLView.as_view(schema=schema, **kwargs), path)

    app.client = SanicTestClient(app)
    return app


def url_string(uri="/graphql", **url_params):
    string = "/graphql"

    if url_params:
        string += "?" + urlencode(url_params)

    return string
