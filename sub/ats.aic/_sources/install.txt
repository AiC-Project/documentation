
Installation
============


Back-end services
-----------------

In the :ref:`openstack-configuration` section, an ``ats.kyaraben`` user was created with
a password. If you didn't create it, please do it now. Then write the
password in a new configuration file:

.. code-block:: sh

    (controller)developer@dev-controller:~/aic$ cat > etc/config-ats.yml <<EOT
    override_environment:
      ats_kyaraben:
        KYARABEN_OPENSTACK_OS_PASSWORD: ************
      ats_authentication:
        ATSAUTH_AUTHENTICATION_OS_USER_TENANT_NAME: aic
      ats_gateway: {}
      ats_senza: {}
    EOT


Optionally, you can provide a FQDN for the frontend. It will be used to configure nginx:

.. code-block:: sh

    (controller)developer@dev-controller:~/aic$ echo \
    "HOSTNAME: fqdn.example.com" >> etc/config-ats.yml



.. note:: If you are on OpenStack Kilo or earlier, add this line to the :file:`config-ats.yml` file:

   ats_kyaraben:
     KYARABEN_OPENSTACK_TEMPLATE: android-kilo.yaml

   The API for device mapping has changed, and separate templates are required to load :code:`data` and :code:`sdcard`
   devices in the correct order.


Create the service and player VMs and install them.

.. code-block:: console

    (controller)developer@dev-controller:~/aic$ aic-stack create ats
    INFO     Creating stack "dev-ats".
    [...]
    INFO     Waiting for port 10.2.0.154:22...
    INFO     Waiting for port 10.2.0.154:22...
    INFO     Waiting for port 10.2.0.154:22...
    Host 10.2.0.154 not found in /home/developer/.ssh/known_hosts
    INFO     Stack "dev-ats" created and available.

    (controller)developer@dev-controller:~/aic$ aic-stack create sdl
    INFO     Creating stack "dev-sdl".
    [...]
    INFO     Waiting for port 10.2.0.156:22...
    INFO     Waiting for port 10.2.0.156:22...
    INFO     Waiting for port 10.2.0.156:22...
    Host 10.2.0.156 not found in /home/developer/.ssh/known_hosts
    INFO     Stack "dev-sdl" created and available.

    (controller)developer@dev-controller:~/aic$ aic install ats
    INFO     Installing ats server.

    PLAY [Deploy an ATS server (AMQP + services)] ********************************* 

    GATHERING FACTS *************************************************************** 
    The authenticity of host '10.2.0.154 (10.2.0.154)' can't be established.
    ECDSA key fingerprint is SHA256:NSn3TV4WVcanEj1/7pKVdaDblx9yyf0r71KHTxciK6s.
    Are you sure you want to continue connecting (yes/no)? yes
    ok: [ats]
    [...]

    docker-host | restart docker -------------------------------------------- 4.89s

    Playbook finished: Mon Jan  4 12:35:05 2016, 36 total tasks.  0:04:51 elapsed. 

    sdl                        : ok=36   changed=31   unreachable=0    failed=0   

    INFO     Install complete.

    (controller)developer@dev-controller:~/aic$ aic install sdl
    INFO     Installing sdl server.
    [...]
    INFO     Install complete.


ROM Images
-----------

Download and extract the VM images:

.. code-block:: sh

    (controller) developer@dev-controller:~/aic$ curl -L https://github.com/AiC-Project/ats.rombuild/releases/download/0.8/aic-kitkat.tar | \
    tar xf - -C images/
    (controller) developer@dev-controller:~/aic$ curl -L https://github.com/AiC-Project/ats.rombuild/releases/download/0.8/aic-lollipop.tar | \
    tar xf - -C images/


The images need to be uploaded in OpenStack Glance.
To upload the Kitkat versions:

.. code-block:: sh

    (controller) developer@dev-controller:~/aic$ aic rom upload images/android/aic-kitkat/gobyt kitkat-tablet
    Reading metadata from [...]
    [...]
    Upload complete.
    (controller) developer@dev-controller:~/aic$ aic rom upload images/android/aic-kitkat/gobyp kitkat-phone
    Reading metadata from [...]
    [...]
    Upload complete.
    $ openstack image list
    +--------------------------------------+----------------------------------------------+--------+
    | ID                                   | Name                                         | Status |
    +--------------------------------------+----------------------------------------------+--------+
    | 202ff9d3-6e20-40b1-81ea-5e9a573c7192 | system-kitkat-phone                          | active |
    | 34c1f24c-d848-4739-a93b-420dbd55d86a | data-kitkat-phone                            | active |
    | 3b4aff17-bec7-438c-ab0a-5e6bf9908a62 | ubuntu-16.04-server-cloudimg-amd64-disk1.img | active |
    [...]


To upload Lollipop:

.. code-block:: sh

    (controller) developer@dev-controller:~/aic$ aic rom upload images/android/aic-lollipop/gobyt lollipop-tablet
    Reading metadata from [...]
    [...]
    (controller) developer@dev-controller:~/aic$ aic rom upload images/android/aic-lollipop/gobyp lollipop-phone
    Reading metadata from [...]
    [...]


Player containers
-----------------

Copy the player images to the Docker host:

.. code-block:: sh

    (controller)developer@dev-controller:~/aic$ aic player upload
    Uploading player images.
    [...]

