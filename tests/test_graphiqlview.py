import pytest

from .util import app, client, url_string


def test_graphiql_is_enabled(client):
    response = client.get(app, uri='/graphql', headers={'Accept': 'text/html'})
    assert response.status_code == 200


def test_graphiql_renders_pretty(client):
    response = client.get(app, uri=url_for('graphql', query='{test}'), headers={'Accept': 'text/html'})
    assert response.status_code == 200
    pretty_response = (
        '{\n'
        '  "data": {\n'
        '    "test": "Hello World"\n'
        '  }\n'
        '}'
    ).replace("\"","\\\"").replace("\n","\\n")

    assert pretty_response in response.data.decode('utf-8')
