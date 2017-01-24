
.. _openstack-configuration:

OpenStack Configuration
=======================

In this section, we'll prepare OpenStack to deploy an AiC installation.

High-level objects like tenants, users and flavors must be created manually.
For everything else (networking, security rules, disks, instances..) we recommend
using the :command:`aic-stack` command, which groups resources into
`Heat <https://wiki.openstack.org/wiki/Heat>`_ stacks, easier to manage and upgrade.

If you have never installed OpenStack and are not sure where to start,
please set aside some time and try the
`Fuel <http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-install-guide.html>`_ installer.

AiC has been tested with the Juno (Mirantis/Fuel 6.1), Kilo (7.0) and Liberty (8.0) versions so far.

Prerequisites:

* Even without Fuel, any other OpenStack distribution should work, provided
  you installed at least the following components.

  - Cinder
  - Glance
  - Heat
  - Neutron
  - Nova

* The Android VMs require a KVM hypervisor. Ubuntu VMs can run in a
  different hypervisor if you really, really need.


Create the tenants and a user for the orchestrator:

.. code-block:: sh

    $ . admin-openrc.sh

    $ openstack project create aic --description 'AiC services and VMs'
    +-------------+----------------------------------+
    | Field       | Value                            |
    +-------------+----------------------------------+
    | description | AiC services and VMs             |
    | enabled     | True                             |
    | id          | 50c368c960374377aafbf9baafab4fb5 |
    | name        | aic                              |
    +-------------+----------------------------------+

    $ openstack project create aic-users --description 'AiC users'
    +-------------+----------------------------------+
    | Field       | Value                            |
    +-------------+----------------------------------+
    | description | AiC users                        |
    | enabled     | True                             |
    | id          | 45d916de26a84c4f89362f1c0868b779 |
    | name        | aic-users                        |
    +-------------+----------------------------------+

    $ pass=$(openssl rand -base64 20)

    $ openstack user create --project aic --password $pass ats.kyaraben

    $ echo pass
    krhtWR9JXr6LPjJm1JupEV5CZFI=

Take note of the password and download the aic-openrc.sh file from the OpenStack dashboard
(``horizon/project/access_and_security``). You will need these later.
If you have chosen another name for the tenant, the file will be named <project>-openrc.sh.

.. note:: There is a simple way to speed up VM management, specifically deletion.
   When a data volume is removed, OpenStack (Cinder service) wipes all the
   bytes by rewriting them, which can take a lot of time. It can be configured
   to skip this operation and free up the space immediately. Be aware of the
   security implication if you remove this feature, as the original bytes
   remain on the unallocated part of the hard disks.

   - Open cinder.conf in all the storage nodes
   - for Kilo and earlier, add: volume_clear_size=10 (0 actually means all)
   - for Liberty and later, add: volume_clear=none
   - Save cinder.conf
   - :command:`sudo service cinder-volume restart`
   - :command:`sudo service cinder-api restart`
   - :command:`sudo service cinder-scheduler restart`

You now need to create a few flavors for the VMs:

.. code-block:: sh

    $ openstack flavor create aic.controller.tiny --ram 4096 --disk 6
    $ openstack flavor create aic.controller.big --ram 8192 --disk 20
    $ openstack flavor create aic.ats --ram 1024 --disk 6
    $ openstack flavor create aic.sdl --ram 8192 --disk 10 --vcpus 2
    $ openstack flavor create aic.android --ram 1024 --disk 2

The big controller flavor is able to build Android images too. The tiny flavor has to use image binaries.

You may also want to increase the quota limits for `secgroups` and `secgroup-rules` for the aic project.
We have set 100 and 1000 respectively since we had no reason to keep them low.

