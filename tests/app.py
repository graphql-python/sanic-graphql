from sanic import Sanic
from sanic_graphql import GraphQLView
from .schema import Schema


def create_app(path='/graphql', **kwargs):
    app = Sanic(__name__)
    app.debug = True
    app.add_route(GraphQLView.as_view(schema=Schema, **kwargs), path)
    return app

if __name__ == '__main__':
    app = create_app(graphiql=True)
    app.run()
