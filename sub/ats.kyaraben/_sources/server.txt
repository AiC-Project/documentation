
Kyaraben server & worker
========================

The server and worker applications are configured via environment variables.

To print their default values:

.. program-output:: kyaraben-server --write-config-defaults
   :prompt:

You can redirect this output to a file and source it from the shell.


The server
^^^^^^^^^^

Once the variables are set, the server can be run with :command:`kyaraben-server`::

    (kyaraben) $ kyaraben-server
    2016-07-27 18:03:58,931 - ats.kyaraben.server - DEBUG  Set up DBMS connection pool...
    2016-07-27 18:03:58,933 - ats.kyaraben.server - DEBUG  Set up AMQP..
    2016-07-27 18:03:58,950 - ats.kyaraben.server - DEBUG  setup done.
    2016-07-27 18:03:58,950 - ats.kyaraben.server - INFO   Server started at ('127.0.0.1', 8084)


All log messages are printed to standard output. You can change the log format to JSON by setting :envvar:`KYARABEN_LOG_JSONFORMAT` = True.

Other options:

.. program-output:: kyaraben-server -h
   :prompt:

The debug toolbar is useful to inspect and troubleshoot requests, it is available under the path ``/_debugtoolbar``.

The ``--db-update`` option is required the first time the server is run, and after version upgrades.
If omitted, it will refuse to start the server in case of pending schema updates.


The worker
^^^^^^^^^^

The server process creates tasks that are meant for *worker processes*. Any number of worker processes can be run, though
each only executes one task at a time.

The workers use the same configuration variables as the server process.

To run a worker process:

.. code-block:: sh

  $ kyaraben-worker
  2016-11-23 16:54:28,054 - ats.kyaraben.worker.main - INFO     event='waiting for messages'

For debugging purposes, a few options are provided:

.. program-output:: kyaraben-worker -h
   :prompt:


Though it should not happen in production, tasks may fail when services are temporarily unavailable. An optional,
dedicated process receives the failed tasks and reschedules them (by delaying from :envvar:`KYARABEN_RETRY_DELAY_MIN`
up to :envvar:`KYARABEN_RETRY_DELAY_MAX` seconds each time, until :envvar:`KYARABEN_RETRY_FAIL_TIMEOUT` has passed and
the task is discarded).

.. code-block:: sh

  $ kyaraben-retry
  2016-11-23 17:03:13,873 - ats.kyaraben.retry.main - INFO     event='waiting for messages'


