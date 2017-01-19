
Bootstrap environment
=====================

The bootstrap environment is used to configure OpenStack and install the build
system within a controller VM.

Python 2.7 is required because the OpenStack and Ansible commands have not been ported to Python 3 yet.
You can install everything inside a Python `virtual environment <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_.
A laptop with any Linux system should be fine.

During the installation, passwords and encryption keys will be generated in the :file:`secrets` directory. You can delete it
when you've done installing all the hosts.


.. code-block:: sh

    $ sudo apt install virtualenv
    $ mkdir aic; cd aic
    $ virtualenv --python=python2.7 bootstrap
    $ source bootstrap/bin/activate
    (bootstrap) $


The ``(bootstrap)`` part of the prompt means you are working within the virtual environment.
The :command:`activate` script changed the :envvar:`PATH` envvar to search in :file:`bootstrap/bin` before anywhere else.
You can exit from the virtual environment anytime by typing :command:`deactivate`, which is a bash function
injected by the :command:`activate` script.

Now download and install the ``ats.aic`` package.

.. code-block:: sh

    (bootstrap) $ mkdir src
    (bootstrap) $ git clone https://github.com/AiC-Project/ats.aic.git src/ats.aic
    (bootstrap) $ pushd src/ats.aic; pip install -r requirements/dev.txt; popd

You should be able to execute the AiC, OpenStack and Ansible clients:

.. code-block:: sh

    (bootstrap) $ type aic aic-inventory aic-stack \
                  openstack ansible >/dev/null && echo "ok"
    ok


Now try the OpenStack client:

.. code-block:: sh

    (bootstrap) $ openstack orchestration build info
    Missing parameter(s):
    Set a username with --os-username, OS_USERNAME, or auth.username


The command starts but cannot authenticate.

Authentication is done through the :file:`aic-openrc.sh` file you previously downloaded
(see `Set environment variables using the OpenStack RC file <http://docs.openstack.org/cli-reference/content/cli_openrc.html>`_).
The same file will be used by the install procedure, as part of the configuration.

.. code-block:: sh

    (bootstrap) $ mkdir etc
    (bootstrap) $ cp /path/to/aic-openrc.sh etc/


If you have SSL endpoints for the OpenStack APIs, you need to copy the
certificate file too. In Mirantis, the certificate file is :file:`public_haproxy.pem`,
but the name may vary for other distributions.

.. code-block:: sh

    (bootstrap) $ cp /path/to/public_haproxy.pem etc/
    (bootstrap) $ echo export OS_CACERT=$(pwd)/etc/public_haproxy.pem >> etc/aic-openrc.sh


To activate both the virtual environment and the OpenStack credentials at the same time, create a small script:

.. code-block:: sh

    (bootstrap) $ echo "source bootstrap/bin/activate" >environment.sh
    (bootstrap) $ echo "source etc/aic-openrc.sh" >>environment.sh


Since the script changes variables and injects functions in the bash environment,
it must be called with :command:`source environment.sh`.
Provide the OpenStack password, then retry:


.. code-block:: sh

    $ source environment.sh
    Please enter your OpenStack Password:
    $ openstack orchestration build info
    +----------+-------------------------+
    | Property | Value                   |
    +----------+-------------------------+
    | api      | {                       |
    |          |   "revision": "unknown" |
    |          | }                       |
    | engine   | {                       |
    |          |   "revision": "unknown" |
    |          | }                       |
    +----------+-------------------------+


The actual output is not important, the command succeeded in authenticating with the
`Heat API <http://developer.openstack.org/api-ref-orchestration-v1.html>`_.


In order to continue, you need a minimal configuration file. The ``cluster``
value will be used as a name prefix - to have for instance production and test
(or development) servers on the same OpenStack tenant.

.. code-block:: sh

    (bootstrap) $ echo "cluster: dev" > etc/config-controller.yml


Another important value is the name of the public network, where the floating ips will
be assigned. In Mirantis 6 and 7, the network is named ``net04_ext``; in version 8 the
name can be changed when installing and is ``admin_floating_net`` by default. If unsure, check
the network topology in the dashboard. If needed, you can share the network among projects.

When you have found the name, write it in the configuration file:


.. code-block:: sh

    (bootstrap) $ echo "floating_net: admin_floating_net" >> etc/config-controller.yml


Create the network and security infrastructure:

.. code-block:: sh

    (bootstrap) $ aic-stack create network
    Creating stack "network".
    [...]
     Stack network CREATE_COMPLETE


If the command takes more than a few seconds, you probably have a version of OpenStack
that does not report the ``CREATE_COMPLETE`` event (i.e. Juno). In this case, just type :kbd:`Control-C`
and verify with :command:`openstack stack show network` or :command:`openstack stack list` that the status is
indeed ``CREATE_COMPLETE``.

Even with multiple clusters during development, the ``network`` stack is
shared. This is done to limit the consumption of cloud resources and to have
readable names for them. If you need to experiment different network layouts or
security groups, it is recommended to use separate tenants.

The new VMs will use public DNS servers, and may not be able to resolve the hostname
contained in ``OS_AUTH_URL``. You can append it to their /etc/hosts file, by adding
the following to :file:`etc/config-controller.yaml`:

.. code-block:: yaml

  additional_hosts:
    -
      name: public.fuel.local
      ip: 10.2.0.136


Now, we need to upload the image of the Ubuntu distribution used by the Linux services.

.. code-block:: sh

    $ aic-stack upload ubuntu
    Checking if ubuntu-16.04-server-cloudimg-amd64-disk1.img already exists.
    Could not find resource ubuntu-16.04-server-cloudimg-amd64-disk1.img
    Downloading the 16.04 Ubuntu image.
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
    [...]
    Uploading to OpenStack...
    +------------------+------------------------------------------------------+
    | Field            | Value                                                |
    +------------------+------------------------------------------------------+
    | checksum         | 0a82289683f10c0f7c20a67d79697fe7                     |
    | container_format | bare                                                 |
    [...]
    | virtual_size     | None                                                 |
    | visibility       | private                                              |
    +------------------+------------------------------------------------------+
    Done.



An empty sdcard image is required too:

.. code-block:: sh

    $ aic-stack upload sdcard
    Checking if sdcard-1g already exists.
    [...]
    Uploading to OpenStack...
    [...]
    Done.


Now create and store an SSH key to use with the servers:

.. code-block:: sh

    (bootstrap) $ openstack keypair create aic | install -m 600 /dev/fd/0 etc/aic.pem


Keep in mind that you will not be able to download the key again from Horizon.

If the AiC git repositories require a deployment key, provide it in the same directory:

.. code-block:: sh

    (bootstrap) $ cp /path/to/git_key etc/

