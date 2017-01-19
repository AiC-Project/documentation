
Using AiC
=========


Connecting with a browser
-------------------------

You can connect to the AiC frontend with the command:

.. code-block:: sh

    (controller) developer@dev-controller:~/aic$ aic browser frontend
    Opening browser.
    Running: sensible-browser https://10.2.0.152:8443
    Created new window in existing browser session.


You can log in with the "ats.kyaraben" user.


User management
---------------

You can create more users in the "aic" tenant, and manage them through OpenStack.
These will have access to both AiC and OpenStack services (create linux vms, etc).
Android VMs do not not count against these user's quota, as AiC has internal per-user limits.

You can tell AiC to authenticate users against a different tenant (possibly with restricted policy, or quota 0).

To do that, create an "aic-users" tenant and change :code:`ATSAUTH_AUTHENTICATION_OS_USER_TENANT_NAME = "aic-users"`
in the file :file:`/etc/supervisor/conf.d/ats-authentication.conf`, then restart the service with :command:`supervisorctl restart ats-auth`

