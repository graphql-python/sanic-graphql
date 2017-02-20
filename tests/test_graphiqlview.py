import pytest

from jinja2 import Environment

from .util import app, client, url_string, create_app


@pytest.mark.parametrize('app', [create_app(graphiql=True)])
def test_graphiql_is_enabled(app, client):
    response = client.get(app,  uri=url_string(), headers={'Accept': 'text/html'})
    assert response.status == 200


@pytest.mark.parametrize('app', [create_app(graphiql=True)])
def test_graphiql_simple_renderer(app, client):
    response = client.get(app, uri=url_string(query='{test}'), headers={'Accept': 'text/html'})
    assert response.status == 200
    pretty_response = (
        '{\n'
        '  "data": {\n'
        '    "test": "Hello World"\n'
        '  }\n'
        '}'
    ).replace('\"','\\\"').replace('\n', '\\n')

    assert pretty_response in response.body.decode('utf-8')


@pytest.mark.parametrize('app', [create_app(graphiql=True, jinja_env=Environment())])
def test_graphiql_jinja_renderer(app, client):
    response = client.get(app, uri=url_string(query='{test}'), headers={'Accept': 'text/html'})
    assert response.status == 200
    pretty_response = (
        '{\n'
        '  "data": {\n'
        '    "test": "Hello World"\n'
        '  }\n'
        '}'
    ).replace('\"','\\\"').replace('\n', '\\n')

    assert pretty_response in response.body.decode('utf-8')


@pytest.mark.parametrize('app', [create_app(graphiql=True, jinja_env=Environment(enable_async=True))])
def test_graphiql_jinja_async_renderer(app, client):
    response = client.get(app, uri=url_string(query='{test}'), headers={'Accept': 'text/html'})
    assert response.status == 200
    pretty_response = (
        '{\n'
        '  "data": {\n'
        '    "test": "Hello World"\n'
        '  }\n'
        '}'
    ).replace('\"','\\\"').replace('\n', '\\n')

    assert pretty_response in response.body.decode('utf-8')


@pytest.mark.parametrize('app', [create_app(graphiql=True)])
def test_graphiql_html_is_not_accepted(app, client):
    response = client.get(app, uri=url_string(), headers={'Accept': 'application/json'})
    assert response.status == 400
