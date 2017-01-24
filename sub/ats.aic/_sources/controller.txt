
Controller environment
======================

The controller is used to build, deploy and manage the AiC components (AOSP, Player, etc.).

The controller environment is very similar to the bootstrap, as it actually uses the same
Python application. The difference is that the controller is always installed on an appropriate
Ubuntu system with all the required libraries, Docker version, and enough disk space
to build the Android images. To make things easier, we'll install the controller inside
OpenStack and continue from there.

Create the controller instance:

.. code-block:: sh

  (bootstrap) $ aic-stack create controller
  INFO     Creating stack "dev-controller".
  +--------------------------------------+----------------+--------------------+---
  | id                                   | stack_name     | stack_status       |
  +--------------------------------------+----------------+--------------------+---
  [...]
  | de761a61-83f0-4fa7-8396-015312374605 | dev-controller | CREATE_IN_PROGRESS |
  +--------------------------------------+----------------+--------------------+---
  [...]
   Stack dev-controller CREATE_COMPLETE 
  INFO     Waiting for port 10.2.0.150:22...
  INFO     Waiting for port 10.2.0.150:22...
  INFO     Waiting for port 10.2.0.150:22...
  # Host 10.2.0.150 found: line 161
  /home/marco/.ssh/known_hosts updated.
  Original contents retained as /home/marco/.ssh/known_hosts.old
  INFO     Stack "dev-controller" created and available.


The server is been created using the `Ubuntu Cloud Image <https://cloud-images.ubuntu.com/>`_.

Install the rest of the packages:


.. code-block:: console

  (bootstrap) $ aic install controller
  INFO     Installing controller server.

  PLAY [Deploy a controller server (build + admin)] ***************************** 

  GATHERING FACTS *************************************************************** 
  The authenticity of host '10.2.0.151 (10.2.0.151)' can't be established.
  ECDSA key fingerprint is SHA256:CTVptNKTZubG3mLC3JCUYm3kP9pgPFCout8myw5e0Fw.
  Are you sure you want to continue connecting (yes/no)? yes


If you see a message like ``fatal: [controller] => SSH Error: Permission denied (publickey)``,
try to connect with :command:`aic-stack ssh controller` and check the SSH key.


Now you should be able to connect to the controller instance.

.. code-block:: console

  (bootstrap) $ aic-stack ssh controller
  INFO     Connecting to server "dev-controller".
  The authenticity of host '10.2.0.150 (10.2.0.150)' can't be established.
  ECDSA key fingerprint is SHA256:ZYrcoVU61xt77PB/glWZJYZT7ppJZGVLqhsPuC8jMuk.
  Are you sure you want to continue connecting (yes/no)? yes
  Warning: Permanently added '10.2.0.150' (ECDSA) to the list of known hosts.
  [...]
  ubuntu@dev-controller:~$


The ``ubuntu`` user can run :command:`sudo` without password, therefore we have a separate user
to actually deploy the services.


.. code-block:: console

  ubuntu@dev-controller:~$ sudo -i
  root@dev-controller:~# su - developer
  developer@dev-controller:~$ cd aic/
  developer@dev-controller:~/aic$ . environment.sh 
  Please enter your OpenStack Password: 
  (controller)developer@dev-controller:~/aic$ aic help
  usage: aic [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]

  aic

  optional arguments:
    --version            show program's version number and exit
    -v, --verbose        Increase verbosity of output. Can be repeated.
    --log-file LOG_FILE  Specify a file to log output. Disabled by default.
    -q, --quiet          Suppress output except warnings and errors.
    -h, --help           Show this help message and exit.
    --debug              Show tracebacks on errors.

  Commands:
    ansible-config  creates or updates ansible.cfg
    complete       print bash completion command
    [...]

