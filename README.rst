|travis| |coveralls| |pypi|

Sanic-GraphQL
=============

Adds `GraphQL <http://graphql.org/>`__ support to your `Sanic <https://github.com/channelcat/sanic>`__ application.

Based on `flask-graphql`_ by `Syrus Akbary`_.

Usage
-----

Just use the ``GraphQLView`` view from ``sanic_graphql``

.. code:: python

    from sanic_graphql import GraphQLView

    app.add_route(GraphQLView.as_view(schema=Schema, graphiql=True), '/graphql')

    # Optional, for adding batch query support (used in Apollo-Client)
    app.add_route(GraphQLView.as_view(schema=Schema, batch=True), '/graphql/batch')

This will add ``/graphql`` endpoint to your app.

Sharing eventloop with Sanic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to pass Sanic's eventloop to GraphQL's ``AsyncioExecutor``, use ``before_start`` listener:

.. code:: python

    @app.listener('before_server_start')
    def init_graphql(app, loop):
        app.add_route(GraphQLView.as_view(schema=Schema, executor=AsyncioExecutor(loop=loop)), '/graphql')


Supported options
~~~~~~~~~~~~~~~~~

-  ``schema``: The ``GraphQLSchema`` object that you want the view to
   execute when it gets a valid request.
-  ``context``: A value to pass as the ``context`` to the ``graphql()``
   function. By default is set to ``dict`` with request object at key ``request``.
-  ``root_value``: The ``root_value`` you want to provide to
   ``executor.execute``.
-  ``pretty``: Whether or not you want the response to be pretty printed
   JSON.
-  ``executor``: The ``Executor`` that you want to use to execute queries. If an ``AsyncioExecutor`` instance is provided,
   performs queries asynchronously within executor's loop.
-  ``graphiql``: If ``True``, may present
   `GraphiQL <https://github.com/graphql/graphiql>`__ when loaded
   directly from a browser (a useful tool for debugging and
   exploration).
-  ``graphiql_template``: Inject a Jinja template string to customize
   GraphiQL.
-  ``jinja_env``: Sets jinja environment to be used to process GraphiQL template. If Jinja's async mode is enabled (by ``enable_async=True``), uses
   ``Template.render_async`` instead of ``Template.render``. If environment is not set, fallbacks to simple regex-based renderer.
-  ``batch``: Set the GraphQL view as batch (for using in
   `Apollo-Client <http://dev.apollodata.com/core/network.html#query-batching>`__
   or
   `ReactRelayNetworkLayer <https://github.com/nodkz/react-relay-network-layer>`__)


You can also subclass ``GraphQLView`` and overwrite
``get_root_value(self, request)`` to have a dynamic root value per
request.

.. code:: python

    class UserRootValue(GraphQLView):
        def get_root_value(self, request):
            return request.user

License
-------

Copyright for portions of project `sanic-graphql`_ are held by `Syrus Akbary`_ as part of project `flask-graphql`_. All other copyright for project `sanic-graphql`_ 
are held by `Sergey Porivaev <https://github.com/grazor>`__.

This project is licensed under MIT License.



.. _`flask-graphql` : https://github.com/graphql-python/flask-graphql
.. _`Syrus Akbary`: https://github.com/syrusakbary
.. _`sanic-graphql`: https://github.com/grazor/sanic-graphql

.. |travis| image:: https://travis-ci.org/graphql-python/sanic-graphql.svg?branch=master
                  :target: https://travis-ci.org/graphql-python/sanic-graphql

.. |coveralls| image:: https://coveralls.io/repos/github/graphql-python/sanic-graphql/badge.svg?branch=master
                     :target: https://coveralls.io/github/graphql-python/sanic-graphql?branch=master

.. |pypi| image:: https://badge.fury.io/py/Sanic-GraphQL.svg
                :target: https://badge.fury.io/py/Sanic-GraphQL
