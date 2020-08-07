[![Build Status](https://travis-ci.org/graphql-python/sanic-graphql.svg?branch=master)](https://travis-ci.org/graphql-python/sanic-graphql)
[![Coverage Status](https://coveralls.io/repos/github/graphql-python/sanic-graphql/badge.svg?branch=master)](https://coveralls.io/github/graphql-python/sanic-graphql?branch=master)
[![PyPI version](https://badge.fury.io/py/Sanic-GraphQL.svg)](https://badge.fury.io/py/Sanic-GraphQL)

Sanic-GraphQL
=============

Adds [GraphQL] support to your [Sanic] application.

Based on [flask-graphql] by [Syrus Akbary].

Usage
-----

Use the `GraphQLView` view from`sanic_graphql`

```python
from sanic_graphql import GraphQLView
from sanic import Sanic

from schema import schema

app = Sanic(name="Sanic Graphql App")

app.add_route(
    GraphQLView.as_view(schema=schema, graphiql=True),
    '/graphql'
)

# Optional, for adding batch query support (used in Apollo-Client)
app.add_route(
    GraphQLView.as_view(schema=schema, batch=True),
    '/graphql/batch'
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

This will add `/graphql` endpoint to your app and enable the GraphiQL IDE.

### Supported options for GraphQLView

 * `schema`: The `GraphQLSchema` object that you want the view to execute when it gets a valid request.
 * `context`: A value to pass as the `context_value` to graphql `execute` function. By default is set to `dict` with request object at key `request`.
 * `root_value`: The `root_value` you want to provide to graphql `execute`.
 * `pretty`: Whether or not you want the response to be pretty printed JSON.
 * `graphiql`: If `True`, may present [GraphiQL](https://github.com/graphql/graphiql) when loaded directly from a browser (a useful tool for debugging and exploration).
 * `graphiql_version`: The graphiql version to load. Defaults to **"1.0.3"**.
 * `graphiql_template`: Inject a Jinja template string to customize GraphiQL.
 * `graphiql_html_title`: The graphiql title to display. Defaults to **"GraphiQL"**.
 * `jinja_env`: Sets jinja environment to be used to process GraphiQL template. If Jinja’s async mode is enabled (by `enable_async=True`), uses 
`Template.render_async` instead of `Template.render`. If environment is not set, fallbacks to simple regex-based renderer.
 * `batch`: Set the GraphQL view as batch (for using in [Apollo-Client](http://dev.apollodata.com/core/network.html#query-batching) or [ReactRelayNetworkLayer](https://github.com/nodkz/react-relay-network-layer))
 * `middleware`: A list of graphql [middlewares](http://docs.graphene-python.org/en/latest/execution/middleware/).
 * `max_age`: Sets the response header Access-Control-Max-Age for preflight requests.
 * `encode`: the encoder to use for responses (sensibly defaults to `graphql_server.json_encode`).
 * `format_error`: the error formatter to use for responses (sensibly defaults to `graphql_server.default_format_error`.
 * `enable_async`: whether `async` mode will be enabled.
 * `subscriptions`: The GraphiQL socket endpoint for using subscriptions in graphql-ws.
 * `headers`: An optional GraphQL string to use as the initial displayed request headers, if not provided, the stored headers will be used.
 * `default_query`: An optional GraphQL string to use when no query is provided and no stored query exists from a previous session. If not provided, GraphiQL will use its own default query.
* `header_editor_enabled`: An optional boolean which enables the header editor when true. Defaults to **false**.
* `should_persist_headers`:  An optional boolean which enables to persist headers to storage when true. Defaults to **false**.


You can also subclass `GraphQLView` and overwrite `get_root_value(self, request)` to have a dynamic root value per request.

```python
class UserRootValue(GraphQLView):
    def get_root_value(self, request):
        return request.user
```


## Contributing
Since v3, `sanic-graphql` code lives at [graphql-server](https://github.com/graphql-python/graphql-server) repository to keep any breaking change on the base package on sync with all other integrations. In order to contribute, please take a look at [CONTRIBUTING.md](https://github.com/graphql-python/graphql-server/blob/master/CONTRIBUTING.md).


## License

Copyright for portions of project [sanic-graphql] are held by [Syrus Akbary] as part of project [flask-graphql]. All other copyright 
for project [sanic-graphql] are held by [Sergey Porivaev].

This project is licensed under MIT License.

  [GraphQL]: http://graphql.org/
  [Sanic]: https://github.com/channelcat/sanic
  [flask-graphql]: https://github.com/graphql-python/flask-graphql
  [Syrus Akbary]: https://github.com/syrusakbary
  [GraphiQL]: https://github.com/graphql/graphiql
  [Apollo-Client]: http://dev.apollodata.com/core/network.html#query-batching
  [ReactRelayNetworkLayer]: https://github.com/nodkz/react-relay-network-layer
  [Sergey Porivaev]: https://github.com/grazor
  [sanic-graphql]: https://github.com/grazor/sanic-graphql
