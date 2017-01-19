
ats.auth server
===============

The server application is configured via environment variables.

To print their default values:

.. program-output:: ats-auth-server --write-config-defaults
   :prompt:

You can redirect this output to a file and source it from the shell.

Once the variables are set, the server can be run with :command:`ats-auth-server`::

    (auth) $ ats-auth-server
    2017-01-17 16:52:44,682 - ats.auth.server.app - DEBUG    event='Set up DBMS connection pool...'
    2017-01-17 16:52:44,694 - ats.auth.server.app - INFO     event="Server started at ('127.0.0.1', 8081)"


All log messages are printed to standard output. You can change the log format to JSON by setting :envvar:`ATSAUTH_LOG_JSONFORMAT` = True.

Other options:

.. program-output:: ats-auth-server -h
   :prompt:

The debug toolbar is useful to inspect and troubleshoot requests, it is available under the path ``/_debugtoolbar``.

