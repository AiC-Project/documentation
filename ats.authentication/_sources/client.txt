
ats.auth client
===============

With the provided client you can create authentication tokens, display
their claims and optionally verify the signature.

.. program-output:: ats-auth help
   :prompt:


Token generation
----------------

.. program-output:: ats-auth help token create
   :prompt:


You have to provide at least a username, either as a parameter or in the OS_USERNAME
environment variable (see `Set environment variables using the OpenStack RC file <http://docs.openstack.org/cli-reference/content/cli_openrc.html>`_).
Likewise, you can provide a password as a parameter, at the prompt or via the OS_PASSWORD variable.

.. code-block:: sh

    $ ats-auth token create --username marco 
    Password for user marco: 
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0NDY1NjQ0OTMuNDE0ODE4LCJzdWIiOiJtYXJjbyIsImlzcyI6ImF0cy5hdXRoIiwiZXhwIjoxNDQ2NTY4MDkzLjQxNDgxOH0.rmmO0NpE9k8Z-Sox7WoBq7LncIwYa9MGUvsjzCQQ1XA


If you want to decode the content of the token, you can do that with the ``--verbose`` option:

.. code-block:: sh

    $ ats-auth token create --username marco --verbose
    Configuration file: ats-auth-client.ini
    Password for user marco: 
    Requesting new token...
    username: marco
    header: {'alg': 'HS256', 'typ': 'JWT'}
    UNVERIFIED claims: {'exp': 1446568241.016732, 'iat': 1446564641.016732, 'iss': 'ats.auth', 'sub': 'marco'}
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0NDY1NjQ2NDEuMDE2NzMyLCJzdWIiOiJtYXJjbyIsImlzcyI6ImF0cy5hdXRoIiwiZXhwIjoxNDQ2NTY4MjQxLjAxNjczMn0.3DWqx1J-DhaFbHurmALqAGkJbFGyKxTn_YTGUwk6KYo


As with all ``cliff``-based commands, the verbose logs are written to stderr, so you can still redirect the relevant stdout content within scripts.

If you also have the jwt_secret value, you can specify it in ``auth-client.ini``:

.. code-block:: ini

    [client]
    jwt_secret = ASDFFGGHJGLKJWELROISUFLDKJFLS

Now the claims will be verified:

.. code-block:: sh

    $ ats-auth token create --username marco --verbose
    Configuration file: ats-auth-client.ini
    Password for user marco: 
    Requesting new token...
    username: marco
    header: {'typ': 'JWT', 'alg': 'HS256'}
    claims: {'exp': 1446568595.9806926, 'iat': 1446564995.9806926, 'sub': 'marco', 'iss': 'ats.auth'}
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0NDY1NjQ5OTUuOTgwNjkyNiwic3ViIjoibWFyY28iLCJpc3MiOiJhdHMuYXV0aCIsImV4cCI6MTQ0NjU2ODU5NS45ODA2OTI2fQ.NO4Xq14r8QxEoNjxytgjEI_on9plMza_kkgXoJ9XRZY

If the secret key is wrong or the token was tampered with, you'll read *Signature verification failed*.



Token revocation
----------------

Revoking a token puts it in a blacklist, therefore denying subsequent requests:

.. code-block:: sh

    $ ats-auth token revoke eyJhbGciOiJIU[...]jiK7StJgRm5jw7pzopfDCxDa0loc
    Logging out user marco
    Token revoked.

When a password is changed, it's a good idea to void all current tokens for a given user:

.. code-block:: sh

    $ ats-auth token revoke-all --as-user marco
    All tokens revoked.



