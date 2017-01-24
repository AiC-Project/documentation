
HTTP API Reference
==================

For the examples, we'll use `httpie <https://httpie.org>`_ (can be installed with pip).

.. code-block:: sh

  $ mkdir ~/.httpie; echo '{"default_options":["--session=default"]}' > ~/.httpie/config.json
  $ pip install httpie
  Collecting httpie
  [...]
  Successfully installed httpie-0.9.9


.. http:post:: /user/login

   Generate a JWT token if the provided credentials are valid.

   **Example request**:

   .. code-block:: sh

      $ http POST :8081/user/login username=marco password=<redacted>

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Length: 210
      Content-Type: application/json; charset=utf-8
      Date: Wed, 18 Jan 2017 14:44:02 GMT
      Server: Python/3.5 aiohttp/1.2.0

      {
          "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhdHMuYXV0aCIsInN1YiI6Im1hcmNvIiwiZXhwIjoxNDg0ODM3MDQyLjg3NTYzMDEsImlhdCI6MTQ4NDc1MDY0Mi44NzU2MzAxfQ.DqBYOAIWuCp2wm6KwEdwrsodYmBK3f9fvQNgqXcTfSE"
      }

   :jsonparam string username: the username to authenticate
   :jsonparam string password: the password to authenticate
   :resheader Content-Type: always application/json
   :statuscode 200: a new token has been issued
   :statuscode 401: the credentials are not valid



.. http:post:: /user/logout

   Revoke an authentication token.

   **Example request**:

   .. code-block:: sh

      $ http POST :8081/user/logout 'Authorization: Bearer eyJ0eXAiOiJKV1[...]sodYmBK3f9fvQNgqXcTfSE'

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream
      Date: Wed, 18 Jan 2017 14:48:39 GMT
      Server: Python/3.5 aiohttp/1.2.0

   :reqheader Authorization: token to revoke
   :resheader Content-Type: always application/octet-stream
   :statuscode 204: the token has been blacklisted


.. http:post:: /user/logout

   Revoke all user tokens.

   **Example request**:

   .. code-block:: sh

      $ http POST :8081/user/logout_all 'X-Auth-UserId: marco'

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream
      Date: Wed, 18 Jan 2017 15:04:11 GMT
      Server: Python/3.5 aiohttp/1.2.0

   :reqheader X-Auth-UserId: user that needs to revoke tokens
   :resheader Content-Type: always application/octet-stream
   :statuscode 204: the tokens have been blacklisted

