
Getting Started
===============

ats.senza is the AiC component responsible for sending data to the sensor emulators. It includes:

* a server application, that receives a JSON object and sends it as a binary packet to a specific sensor of a specific VM.

* a client application, to be used from the command line.

The sensor data is intended for live consumption and testing. There is no
feedback mechanism through the senza API. A getprop command can be issued
with adb to retrieve the current state of the sensors.


Installation
------------

The application requires Python 3.5, and works fine in a virtual environment.

After cloning the source code:

.. code-block:: console

  $ git clone git@git.rnd.alterway.fr:aic_ats/ats.senza.git
  $ git clone git@git.rnd.alterway.fr:aic_ats/ats.util.git
  $ git clone git@git.rnd.alterway.fr:aic_ats/ats.client.git

you can install it in development mode

.. code-block:: console

  $ cd ats.senza
  $ pip3 install -r requirements/dev.txt

