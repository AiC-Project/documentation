
Getting Started
===============

Kyaraben is the AiC component responsible for the orchestration of Android Virtual Machines (in short, AVM)
and related container services. It includes:

* a :command:`kyaraben-server` application, to handle client requests and create orchestration tasks

* a :command:`kyaraben-worker` application, to execute orchestration tasks.

* a :command:`kyaraben-retry` application, to reschedule failed tasks.

* a :command:`kyaraben` client, to create / destroy / list AVMs, media files, applications, tests etc.


Kyaraben requires an OpenStack installation (Kilo or later) with the Keystone, Nova, Heat, Glance and Neutron services.

A Postgres database and RabbitMQ are also required to store application data and the task queues.


Installation
------------

To configure OpenStack for AiC, see `Configuring OpenStack for AiC <http://link.to.some.where/>`_

Kyaraben is usually deployed and configured with the :command:`ats.aic` wrapper. If you really
need to install it for development, you can do it in a Python 3.5 virtualenv with:

.. code-block:: sh

  $ pyvenv-3.5 kyaraben
  $ . kyaraben/bin/activate
  (kyaraben) $ mkdir kyaraben/src; cd kyaraben/src
  (kyaraben) $ git clone https://github.com/AiC-Project/ats.util.git
  (kyaraben) $ git clone https://github.com/AiC-Project/ats.client.git
  (kyaraben) $ git clone https://github.com/AiC-Project/ats.kyaraben.git
  (kyaraben) $ cd ats.kyaraben
  (kyaraben) $ pip install -r requirements/dev.txt
  (kyaraben) $ kyaraben --version
  kyaraben 0.8


