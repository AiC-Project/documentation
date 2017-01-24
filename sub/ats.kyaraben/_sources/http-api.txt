
HTTP API Reference
==================

For the examples, we'll use `httpie <https://httpie.org>`_ (can be installed with pip).
We'll omit CONTENT-LENGTH, DATE and SERVER response headers.

.. code-block:: sh

  $ mkdir ~/.httpie; echo '{"default_options":["--session=default"]}' > ~/.httpie/config.json
  $ pip install httpie
  Collecting httpie
  [...]
  Successfully installed httpie-0.9.9


When directly connected to the kyaraben server beyond the authentication component (we'll assume
port localhost:8084) the current user can be specified with the X-Auth-UserId header:

404 errors are possible in most cases, and will happen - for security reasons - even when the user
does not exist, or the user exists but does not have permission to access the resource.

.. code-block:: sh

  $ http :8084/user/whoami
  HTTP/1.1 401 Unauthorized
  Content-Type: application/json; charset=utf-8

  {
      "error": "Missing authentication header"
  }

  $ http :8084/user/whoami X-Auth-UserId:marco
  HTTP/1.1 200 OK
  Content-Type: application/json; charset=utf-8

  {
      "user": {
          "userid": "marco"
      }
  }


Since we defined a default session for httpie, the user header is persistent, there is no need to repeat it.

.. code-block:: sh

  $ http :8084/user/whoami
  HTTP/1.1 200 OK
  Content-Type: application/json; charset=utf-8

  {
      "user": {
          "userid": "marco"
      }
  }


.. http:get:: /android

   Return the Android VMs that belong to a user

   **Example request**:

   .. code-block:: sh

      $ http :8084/android

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "avms": [
              {
                  "avm_id": "f40d2ec4b55911e6a436fa163e316d19",
                  "avm_name": "f40d2ec4",
                  "avm_owner": "marco",
                  "campaign_id": "",
                  "image": "kitkat-tablet",
                  "project_id": "fb651ee0b31d11e6a436fa163e316d19",
                  "status": "READY",
                  "ts_created": "2016-11-28T11:01:03Z",
                  "uptime": 22226.51023
              },
              {
                  "avm_id": "ededb9ccb58c11e6a436fa163e316d19",
                  "avm_name": "ededb9cc",
                  "avm_owner": "marco",
                  "campaign_id": "",
                  "image": "lollipop-phone",
                  "project_id": "fb651ee0b31d11e6a436fa163e316d19",
                  "status": "READY",
                  "ts_created": "2016-11-28T17:05:57Z",
                  "uptime": 334.477165
              }
          ]
      }

   :requestheader X-Auth-UserId: the user who created and owns the virtual machines.
                                 If the user does not exist, no error is reported and an empty list is returned
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json uuid avm_id: unique identifier
   :>json string avm_name: user-provided name, or generated from avm_id if not provided
   :>json string avm_owner: the user who owns the AVM
   :>json uuid campaign_id: for async vms, id of the test campaign
   :>json string image: Android image used to instantiate the AVM
   :>json uuid project_id: parent project of the AVM
   :>json string status: one of (QUEUED, CREATING, READY, DELETING, DELETED, ERROR)
   :>json iso8601 ts_created: timestamp of the creation
   :>json float uptime: longevity of the VM, in seconds



.. http:get:: /android/(string:avm_id)

   Status and metadata of an Android Virtual Machine.

   **Example request**:

   .. code-block:: sh

      $ http :8084/android/30adc730b63111e6a436fa163e316d19

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "avm": {
              "avm_id": "30adc730b63111e6a436fa163e316d19",
              "avm_name": "first vm",
              "avm_owner": "marco",
              "campaign_id": "",
              "hwconfig": {
                  "dpi": 160,
                  "enable_battery": 0,
                  "enable_camera": 1,
                  "enable_gps": 1,
                  "enable_gsm": 1,
                  "enable_nfc": 0,
                  "enable_record": 0,
                  "enable_sensors": 1,
                  "height": 800,
                  "width": 1280
              },
              "image": "kitkat-tablet",
              "project_id": "e1df30bcb61c11e6a436fa163e316d19",
              "status": "READY",
              "status_reason": "",
              "status_ts": "2016-11-29T12:42:56Z",
              "ts_created": "2016-11-29T12:41:46Z",
              "uptime": 1648.454066
          }
      }

   :requestheader X-Auth-UserId: the user who created and owns the virtual machine
   :param avm_id: the virtual machine identifier
   :statuscode 200: no error
   :statuscode 404: there is no vm identified by avm_id, or it exists but does not belong to the user, or the user itself does not exist
   :resheader Content-Type: always application/json
   :>json uuid avm_id: virtual machine identifier
   :>json string avm_name: given or generated VM name
   :>json string avm_owner: the user who owns the AVM
   :>json uuid campaign_id: the id of the test campaign (for async vms)
   :>json object hwconfig: the environment configuration provided at time of creation
   :>json string image: Android image used to create the VM
   :>json uuid project_id: parent project of the AVM
   :>json string status: one of (QUEUED, CREATING, DELETING, READY, DELETED, ERROR)
   :>json string status_reason: status details (when status=ERROR)
   :>json iso8601 status_ts: timestamp of the status
   :>json iso8601 ts_created: timestamp of the creation
   :>json float uptime: longevity of the VM, in seconds



.. http:get:: /android/(string:avm_id)/apk

   List of the third party, enabled packages installed in a VM.
   System or disabled applications are not returned.

   **Example request**:

   .. code-block:: sh

      $ http :8084/android/78292832b70011e69093fa163e5f2779/apk

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "packages": [
              "com.example.android.apis",
              "com.android.gesture.builder"
          ]
      }

   :requestheader X-Auth-UserId: a user who has access to the virtual machine
   :param avm_id: the virtual machine identifier
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json array packages: list of package names



.. http:get:: /android/(string:avm_id)/command/(string:command_id)

   Retrieve output of a remote command run on a VM.

   This is used to capture logs of test runs, monkey tool and apk installation.

   **Example request**:

   .. code-block:: sh

      $ http :8084/android/78292832b70011e69093fa163e5f2779/command/30c88f2cb71011e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "results": [
              {
                  "returncode": "0",
                  "status": "READY",
                  "stderr": "3880 KB/s (872273 bytes in 0.219s)",
                  "stdout": "pkg: /data/local/tmp/282831ecb71011e69093fa163e5f2779.apk\nSuccess"
              }
          ]
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the virtual machine identifier
   :param command_id: a command identifier
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json string returncode: the return code of the adb command
   :>json string status: one of (QUEUED, RUNNING, READY, ERROR)
   :>json string stderr: the captured standard error
   :>json string stdout: the captured standard output


.. http:get:: /android/(string:avm_id)/properties

      Retrieve the current values of `Android properties <https://developer.android.com/reference/android/util/Property.html>`_.

   **Example request**:

   .. code-block:: sh

      $ http :8084/android/78292832b70011e69093fa163e5f2779/properties

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "properties": {
              "aicVM.gles": "1",
              "aicVM.gles.renderer": "1",
              "aicVM.inited": "1",
              "aicd.ac.online": "1",
              "aicd.accelerometer.x": "0.000000",
              "aicd.accelerometer.y": "9.776219",
              "aicd.accelerometer.z": "0.813417",
              "...": "...",
              "sys.settings_system_version": "12",
              "sys.sysctl.extra_free_kbytes": "5625",
              "sys.sysctl.tcp_def_init_rwnd": "60",
              "sys.usb.config": "adb",
              "sys.usb.state": "adb",
              "wifi.interface": "eth1",
              "wifi.interface.mac": "fa:16:3e:6e:9d:aa",
              "wlan.driver.status": "ok"
          }
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the virtual machine identifier
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json object properties: an object of {property_name: property_value, ...}


.. http:get:: /android/(string:avm_id)/testrun

   List the test packages installed in a VM.

   .. note::

      This API is misplaced. It's more the test equivalent of `GET /android/{android_id}/apk`
      than the counterpart to `PUT /android/{android_id}/testrun`.

   **Example request**:

   .. code-block:: sh

      $ http :8084/android/78292832b70011e69093fa163e5f2779/testrun

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "packages": {
              "com.example.android.apis/.app.LocalSampleInstrumentation": "com.example.android.apis",
              "com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner": "com.zenika.aic.core.libs.test"
          }
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the virtual machine identifier
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json object packages: an object of the form {package_name: target, ...}


.. http:get:: /android/(string:avm_id)/totp

      Generate a Time-Based One-Time Password to connect to the Android display. The password is valid for 30 seconds.

   **Example request**:

   .. code-block:: sh

      $ http :8084/android/78292832b70011e69093fa163e5f2779/totp

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "totp": "226688"
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the virtual machine identifier
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json string totp: a password to be sent to the remote VNC server, or the reverse proxy


.. http:post:: /android

   Create an Android VM and assign it to the current user.

   A positive response means the creation of the AVM has been started.
   As soon as the resources have been created and the services deployed, the VM status
   becomes READY, even though the VM is still booting up.

   Errors coming from OpenStack (for instance, if the creation would cause the
   user to go over the quota allocated to the tenant, or a networking issue)
   will leave the AVM resource with a status of ERROR and the creation tasks
   automatically rescheduled, to be retried when the (hopefully transient)
   problem is fixed. More details about such errors (and exception traceback)
   can be found either in worker logs, or in the SQL database (column avms.status_reason).

   The only required values are *project_id* and *image*.

   **Example request**:

   .. code-block:: sh

      $ http post :8084/android \
      project_id=e1df30bcb61c11e6a436fa163e316d19 \
      image=kitkat-tablet \
      hwconfig:='{"width":1280,"height":800,"enable_battery":0}' \
      avm_name=first_avm

   **Example response**:

   .. code-block:: http

      HTTP/1.1 201 Created
      Content-Type: application/json; charset=utf-8

      {
          "avm_id": "e005e700b62f11e6a436fa163e316d19"
      }

   :requestheader X-Auth-UserId: a user who will own the AVM
   :<json uuid project_id: parent project of the AVM
   :<json string image: Android image to use
   :<json string avm_name: optional VM name. If missing, part of the id will be used
   :<json object hwconfig: object with one or more of the following keys
   :<json integer hwconfig["width"]: screen width
   :<json integer hwconfig["height"]: screen height
   :<json integer hwconfig["dpi"]: screen DPI
   :<json integer hwconfig["enable_sensors"]: 0/1
   :<json integer hwconfig["enable_battery"]: 0/1
   :<json integer hwconfig["enable_gps"]: 0/1
   :<json integer hwconfig["enable_camera"]: 0/1
   :<json integer hwconfig["enable_record"]: 0/1
   :<json integer hwconfig["enable_gsm"]: 0/1
   :<json integer hwconfig["enable_nfc"]: 0/1
   :statuscode 201: the creation of AVM and services has started
   :statuscode 400: malformed request (response contains the expected JSON schema)
   :resheader Content-Type: always application/json
   :>json uuid avm_id: unique identifier


.. http:post:: /android/(string:avm_id)/apk/(string:apk_id)

   Install an application in a running VM.
   The APK file must have been previously uploaded to the project.
   The request returns the ID of an asynchronous command. The application
   can be reinstalled multiple times without uninstalling.

   **Example request**:

   .. code-block:: sh

      $ http post :8084/android/78292832b70011e69093fa163e5f2779/apk/282831ecb71011e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 202 Accepted
      Content-Type: application/json; charset=utf-8

      {
          "command_id": "e9c40926b71911e69093fa163e5f2779"
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the virtual machine identifier
   :param apk_id: the APK identifier
   :statuscode 202: no error
   :resheader Content-Type: always application/json
   :>json uuid command_id: a command identifier


.. http:post:: /android/(string:avm_id)/monkey

   Execute the `UI/Application Exerciser Monkey <https://developer.android.com/studio/test/monkey.html>`_ on an application.

   **Example request**:

   .. code-block:: sh

      $ http post :8084/android/78292832b70011e69093fa163e5f2779/monkey \
      packages:='["com.uberspot.a2048","com.example.android.apis"]' \
      event_count=100

   **Example response**:

   .. code-block:: http

      HTTP/1.1 202 Accepted
      Content-Type: application/json; charset=utf-8

      {
          "command_id": "e0f7a8eab71711e69093fa163e5f2779"
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the virtual machine identifier
   :statuscode 202: no error
   :resheader Content-Type: always application/json
   :>json uuid command_id: a command identifier



.. http:post:: /android/(string:avm_id)/testrun

   Run instrumented test packages.

   **Example request**:

   .. code-block:: sh

      $ http post :8084/android/78292832b70011e69093fa163e5f2779/testrun package=com.uberspot.a2048

   **Example response**:

   .. code-block:: http

      HTTP/1.1 202 Accepted
      Content-Type: application/json; charset=utf-8

      {
          "command_id": "8d9f07a6b72111e69093fa163e5f2779"
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: uuid of the VM
   :<json string package: name of the test package to run
   :statuscode 202: no error
   :>json uuid command_id: a command identifier


.. http:put:: /android

   Changes metadata of an Android VM (currently only the name).

   **Example request**:

   .. code-block:: sh

      $ http put :8084/android/78292832b70011e69093fa163e5f2779 avm_name=totoro

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: uuid of the VM
   :<json string avm_name: new VM name
   :statuscode 204: the name of the VM has been changed


.. http:delete:: /android/(string:avm_id)

   Remove an AVM and its associated services (video rendering, web console, adb).

   Like its creation counterpart, this operation is asynchronous and returns a positive response
   as soon as the removal has started. Failures to delete Heat stacks are not handled by this API.

   **Example request**:

   .. code-block:: sh

      $ http delete :8084/android/30adc730b63111e6a436fa163e316d19

   **Example response**:

   .. code-block:: http

      HTTP/1.1 202 Accepted

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the identifier of the AVM to remove
   :statuscode 202: the removal of AVM and services has started
   :statuscode 404: the AVM does not exist, or does not belong to the user, or the user does not exist


.. http:get:: /images

   Returns the list of the available Android images.

   **Example request**:

   .. code-block:: sh

      $ http :8084/images

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "images": [
              {
                  "android_version": 4,
                  "image": "kitkat-tablet"
              },
              {
                  "android_version": 4,
                  "image": "kitkat-phone"
              },
              {
                  "android_version": 5,
                  "image": "lollipop-tablet"
              },
              {
                  "android_version": 5,
                  "image": "lollipop-phone"
              }
          ]
      }

   :requestheader X-Auth-UserId: a user who has access to the AVM
   :param avm_id: the virtual machine identifier
   :statuscode 200: no error
   :>json string image: the prefix to be used when retrieving system and data images in OpenStack Glance
   :>json int android_version: the major version of Android, used to link the right OpenGL libraries in the player containers


.. http:get:: /projects

   Returns the projects the user has access to.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK

      {
          "projects": [
              {
                  "project_id": "5416126cb64b11e69093fa163e5f2779",
                  "project_name": "foo",
                  "status": "READY"
              }
          ]
      }

   :requestheader X-Auth-UserId: the user who created, or with whom the projects are shared.
                                 If the user does not exist, no error is reported and an empty list is returned
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json uuid project_id: unique identifier
   :>json string project_name: user-provided name
   :>json string status: one of (QUEUED, CREATING, READY, DELETING, DELETED, ERROR)


.. http:get:: /projects/(string:project_id)

   Status and metadata of a project.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/5416126cb64b11e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "project": {
              "count_avms": 0,
              "project_id": "5416126cb64b11e69093fa163e5f2779",
              "project_name": "foo",
              "status": "READY",
              "status_reason": "",
              "status_ts": "2016-11-29T15:48:53Z",
              "sum_avms_uptime": 0.0
          }
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or it exists but does not belong to the user, or the user itself does not exist
   :resheader Content-Type: always application/json
   :>json integer count_avms: number of Virtual Machines in the project
   :>json uuid project_id: uuid of the project
   :>json uuid project_name: user-provided name
   :>json string status: one of (QUEUED, CREATING, READY, DELETING, DELETED, ERROR)
   :>json string status_reason: status details (when status=ERROR)
   :>json iso8601 status_ts: timestamp of the status
   :>json float sum_avms_uptime: total longevity of the VMs in the project, in seconds


.. http:get:: /projects/(string:project_id)/apk

   List the APK files contained in a project.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/722de0eeb70011e69093fa163e5f2779/apk

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "apks": [
              {
                  "apk_id": "282831ecb71011e69093fa163e5f2779",
                  "filename": "com.uberspot.a2048_23.apk",
                  "package": "com.uberspot.a2048",
                  "project_id": "722de0eeb70011e69093fa163e5f2779",
                  "status": "READY",
                  "testsource_id": ""
              },
              {
                  "apk_id": "8a2d63d2b7a911e69093fa163e5f2779",
                  "filename": "com.zenika.aic.core.libs.test-2.apk",
                  "package": "com.zenika.aic.core.libs.test",
                  "project_id": "722de0eeb70011e69093fa163e5f2779",
                  "status": "READY"
                  "testsource_id": ""
              }
          ]
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or it exists but does not belong to the user, or the user itself does not exist
   :resheader Content-Type: always application/json
   :>json uuid apk_id: the APK identifier
   :>json string filename: the original name of the uploaded file
   :>json string package: package name from AndroidManifest.xml
   :>json uuid project_id: uuid of the project
   :>json string status: one of (QUEUED, UPLOADING, COMPILING DSL, COMPILING JAVA, READY, DELETING, DELETED, ERROR)
   :>json uuid testsource_id: identifier of the test source file (if the apk was compiled) or empty string if the apk was uploaded


.. http:get:: /projects/(string:project_id)/apk/(string:apk_id)

   Retrieve information about an APK.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/722de0eeb70011e69093fa163e5f2779/apk/282831ecb71011e69093fa163e5f2779

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "apk": {
              "apk_id": "282831ecb71011e69093fa163e5f2779",
              "filename": "com.uberspot.a2048_23.apk",
              "package": "com.uberspot.a2048",
              "project_id": "722de0eeb70011e69093fa163e5f2779",
              "status": "READY",
              "status_reason": ""
          }
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param apk_id: the APK identifier
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or no apk identified by apk_id
   :resheader Content-Type: always application/json
   :>json uuid apk_id: the APK identifier
   :>json string filename: the original name of the uploaded file
   :>json string package: package name from AndroidManifest.xml
   :>json uuid project_id: uuid of the project
   :>json string status: one of (QUEUED, UPLOADING, COMPILING DSL, COMPILING JAVA, READY, DELETING, DELETED, ERROR)
   :>json string status_reason: status details (when status=ERROR)


.. http:get:: /projects/(string:project_id)/camera

   List the camera files contained in a project.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/722de0eeb70011e69093fa163e5f2779/camera

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "camera_files": [
              {
                  "camera_id": "15a56ea8b87911e69093fa163e5f2779",
                  "filename": "ubuntu-logo.png",
                  "project_id": "722de0eeb70011e69093fa163e5f2779",
                  "status": "READY"
              }
          ]
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or it exists but does not belong to the user, or the user itself does not exist
   :resheader Content-Type: always application/json
   :>json uuid camera_id: the camera file identifier
   :>json string filename: the original name of the uploaded file
   :>json uuid project_id: uuid of the project
   :>json string status: one of (UPLOADING, READY, DELETING, DELETED, ERROR)


.. http:get:: /projects/(string:project_id)/campaigns

   List the test campaigns in a project.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/63f49082dbf811e690e6fa163e15ccce/campaigns

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "campaigns": [
              {
                  "campaign_id": "8bbe5d58dc0411e690e6fa163e15ccce",
                  "campaign_name": "lovely-big-cobra",
                  "project_id": "63f49082dbf811e690e6fa163e15ccce",
                  "status": "READY"
              }
          ]
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or it exists but does not belong to the user, or the user itself does not exist
   :resheader Content-Type: always application/json
   :>json uuid campaign_id: uuid of the campaign
   :>json string campaign_name: custom (user defined or generated) campaign name
   :>json string status: one of (QUEUED, RUNNING, READY, DELETING, DELETED, ERROR)


.. http:get:: /projects/(string:project_id)/campaigns/(string:campaign_id)

   Retrieve information about a test campaign.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/63f49082dbf811e690e6fa163e15ccce/campaigns/8bbe5d58dc0411e690e6fa163e15ccce

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "campaign": {
              "campaign_id": "8bbe5d58dc0411e690e6fa163e15ccce",
              "campaign_name": "lovely-big-cobra",
              "campaign_status": "READY",
              "progress": 1.0,
              "project_id": "63f49082dbf811e690e6fa163e15ccce",
              "tests": [
                  {
                      "hwconfig": {
                          "dpi": 160,
                          "enable_battery": 1,
                          "enable_camera": 1,
                          "enable_gps": 1,
                          "enable_gsm": 1,
                          "enable_nfc": 0,
                          "enable_record": 0,
                          "enable_sensors": 1,
                          "height": 600,
                          "width": 800
                      },
                      "image": "lollipop-phone",
                      "package": "com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner",
                      "status": "READY",
                      "stdout": "INSTRUMENTATION_STATUS: numtests=2\nINSTRUMENTATION_STATUS: stream=\ncom.zenika.aic.core.libs.ParserTest [...]"
                  }
              ]
          }
      }

   :requestheader X-Auth-UserId: a user who has access to the campaign
   :param project_id: uuid of the project
   :param campaign_id: uuid of the campaign
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or no campaign
   :resheader Content-Type: always application/json
   :>json uuid campaign_id: uuid of the campaign
   :>json string campaign_name: custom (user defined or generated) campaign name
   :>json string campaign_status: one of (QUEUED, RUNNING, READY, DELETING, DELETED, ERROR)
   :>json float progress: completion status of the campaign
   :>json object hwconfig: the environment configuration for the VM
   :>json string image: Android image used to create the VM
   :>json string package: instrumented test package
   :>json string status: one of (QUEUED, RUNNING, READY, ERROR)



.. http:delete:: /projects/(string:project_id)/campaigns/(string:campaign_id)

   Remove an existing test campaign (either running, or finished).

   **Example request**:

   .. code-block:: sh

      $ http delete :8084/projects/63f49082dbf811e690e6fa163e15ccce/campaigns/8bbe5d58dc0411e690e6fa163e15ccce

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param campaign_id: uuid of the campaign
   :statuscode 204: the campaign has been deleted


.. http:get:: /projects/(string:project_id)/testsources

   List the DSL files in a project.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/722de0eeb70011e69093fa163e5f2779/testsources

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "testsources": [
              {
                  "apk_id": "0e18f032dca611e690e7fa163e15ccce",
                  "apk_status": "READY",
                  "apk_status_reason": "",
                  "filename": "test1.aic",
                  "project_id": "722de0eeb70011e69093fa163e5f2779",
                  "status": "READY",
                  "testsource_id": "ef8ef4ccdca511e690e7fa163e15ccce"
              },
              {
                  "apk_id": "",
                  "apk_status": "COMPILING JAVA",
                  "apk_status_reason": "",
                  "filename": "test2.aic",
                  "project_id": "722de0eeb70011e69093fa163e5f2779",
                  "status": "READY",
                  "testsource_id": "f107efd4dca511e690e7fa163e15ccce"
              },
          ]
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or it exists but does not belong to the user, or the user itself does not exist
   :resheader Content-Type: always application/json
   :>json uuid apk_id: the APK identifier (if the file has been compiled), or empty string
   :>json string apk_status: one of (QUEUED, UPLOADING, COMPILING DSL, COMPILING JAVA, READY, DELETING, DELETED, ERROR)
   :>json string apk_status_reason: status details (when apk_status=ERROR)
   :>json string filename: the original name of the uploaded file
   :>json uuid project_id: uuid of the project
   :>json string status: one of (UPLOADING, READY)
   :>json uuid testsource_id: identifier of the test source file


.. http:get:: /projects/(string:project_id)/testsources/(string:testsource_id)

   Download the content of a test source (DSL).

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/722de0eeb70011e69093fa163e5f2779/testsources/eaefe8b8b87911e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Length: 204
      Content-Type: text/plain; charset=utf-8

      Feature: "Best feature ever"
         Scenario: "Best scenario ever"
            Set sensor TYPE_LIGHT at 42
            Take a screenshot
         End

         Scenario: "Worst scenario ever"
            Set battery level at 1
         End
      End

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param testsource_id: identifier of the test source file
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or no testsource identified by testsource_id
   :resheader Content-Type: always text/plain


.. http:get:: /projects/(string:project_id)/testsources/(string:testsource_id)/metadata

   Retrieve information about a test source.

   **Example request**:

   .. code-block:: sh

      $ http :8084/projects/722de0eeb70011e69093fa163e5f2779/testsources/eaefe8b8b87911e69093fa163e5f2779/metadata

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "testsource": {
              "apk_id": "",
              "apk_status": "",
              "apk_status_reason": "",
              "filename": "test.aic",
              "project_id": "722de0eeb70011e69093fa163e5f2779",
              "status": "READY",
              "testsource_id": "eaefe8b8b87911e69093fa163e5f2779"
          }
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param testsource_id: identifier of the test source file
   :statuscode 200: no error
   :statuscode 404: there is no project identified by project_id, or no testsource identified by testsource_id
   :resheader Content-Type: always application/json
   :>json uuid apk_id: the APK identifier (if the file has been compiled), or empty string
   :>json string apk_status: one of (QUEUED, UPLOADING, COMPILING DSL, COMPILING JAVA, READY, DELETING, DELETED, ERROR)
   :>json string apk_status_reason: status details (when apk_status=ERROR)
   :>json string filename: the original name of the uploaded file
   :>json uuid project_id: uuid of the project
   :>json string status: one of (UPLOADING, READY)
   :>json uuid testsource_id: identifier of the test source file


.. http:post:: /projects

   Create a project and assign it to the current user.

   A positive response means the creation of the project has been started.
   When the project creation is finalized, its status becomes READY.

   **Example request**:

   .. code-block:: sh

      $ http post :8084/projects project_name=peace

   **Example response**:

   .. code-block:: http

      HTTP/1.1 201 Created
      Content-Type: application/json; charset=utf-8

      {
          "project_id": "3d7cff8eb6ff11e69093fa163e5f2779"
      }

   :requestheader X-Auth-UserId: the user who will own the project
   :<json string project_name: user-provided name, need not be unique
   :statuscode 201: the creation of the project has started
   :resheader Content-Type: always application/json
   :>json uuid project_id: unique identifier

.. http:post:: /projects/(string:project_id)/apk

   Upload an APK file to a project.

   **Example request**:

   .. code-block:: sh

      $ http --form :8084/projects/e8248ab0baf111e69093fa163e5f2779/apk file@com.uberspot.a2048_23.apk 

   **Example response**:

   .. code-block:: http

      HTTP/1.1 201 Created
      Content-Type: application/json; charset=utf-8

      {
          "apk_id": "5c96b552baf311e69093fa163e5f2779"
      }


   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 201: the upload of the apk has started
   :resheader Content-Type: always application/json
   :>json uuid apk_id: the APK identifier


.. http:post:: /projects/(string:project_id)/camera

   Upload a camera file to a project. The file can be an image or movie, and
   will be converted if needed.

   **Example request**:

   .. code-block:: sh

      $ http --form :8084/projects/722de0eeb70011e69093fa163e5f2779/camera file@ubuntu-logo.png 

   **Example response**:

   .. code-block:: http

      HTTP/1.1 201 Created
      Content-Type: application/json; charset=utf-8

      {
          "camera_file_id": "15a56ea8b87911e69093fa163e5f2779"
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 201: the upload/conversion of the media file has started
   :resheader Content-Type: always application/json
   :>json uuid camera_file_id: the camera file identifier


.. http:post:: /projects/(string:project_id)/campaigns

   Create a test campaign.

   **Example request**:

   .. code-block:: sh

      $ http post :8084/projects/63f49082dbf811e690e6fa163e15ccce/campaigns campaign_name=my-campaign tests:='[{"image":"kitkat-tablet", "hwconfig":{"dpi":160,"enable_battery":1,"enable_camera":1,"enable_gps":1,"enable_gsm":1,"enable_nfc":0,"enable_record":0,"enable_sensors":1,"height":600,"width": 800}, "apks":["54cf0536dbfa11e690e6fa163e15ccce","5b1c0a06dbfa11e690e6fa163e15ccce","10971afadca611e690e7fa163e15ccce"], "packages":["com.example.android.apis","com.android.gesture.builder"]}]'

   **Example response**:

   .. code-block:: http

      HTTP/1.1 202 Accepted
      Content-Type: application/json; charset=utf-8

      {
          "campaign_id": "5ee2fbc8dcb211e690e7fa163e15ccce"
      }


   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :>json string campaign_name: custom campaign name, will generate one if missing
   :>json object tests: list of testruns to create
   :>json string image: Android image used to create the VM
   :>json object hwconfig: configuration of the VM
   :>json object apks: list of APKs to install
   :>json object packages: list of packages under test
   :statuscode 202: the creation of the campaign has started
   :resheader Content-Type: always application/json
   :>json uuid campaign_id: id of the new test campaign


.. http:post:: /projects/(string:project_id)/testsources

   Upload a test source to a project.

   **Example request**:

   .. code-block:: sh

      $ http --form :8084/projects/722de0eeb70011e69093fa163e5f2779/testsources file@test.aic

   **Example response**:

   .. code-block:: http

      HTTP/1.1 201 Created
      Content-Type: application/json; charset=utf-8

      {
          "testsource_id": "eaefe8b8b87911e69093fa163e5f2779"
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 201: the file has been uploaded
   :resheader Content-Type: always application/json
   :>json uuid testsource_id: identifier of the test source file


.. http:post:: /projects/(string:project_id)/testsources/(string:testsource_id)/apk

   Compile a test source to an APK file.

   **Example request**:

   .. code-block:: sh

      $ http post :8084/projects/63f49082dbf811e690e6fa163e15ccce/testsources/39c9ad06dca711e690e7fa163e15ccce/apk

   **Example response**:

   .. code-block:: http

      HTTP/1.1 202 Accepted
      Content-Type: application/json; charset=utf-8

      {
          "apk_id": "82db80fadca711e690e7fa163e15ccce"
      }

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :statuscode 202: the testsource is being compiled
   :resheader Content-Type: always application/json
   :>json uuid apk_id: the APK identifier of the test application


.. http:put:: /projects/(string:project_id)

   Changes metadata of a project (currently only the name).

   **Example request**:

   .. code-block:: sh

      $ http put :8084/projects/722de0eeb70011e69093fa163e5f2779 project_name=qwerty

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :<json string avm_name: new project name
   :statuscode 204: the name of the project has been changed


.. http:put:: /projects/(string:project_id)/testsources/(string:testsource_id)

   Update the content of a test source. Filename will be updated too.

   **Example request**:

   .. code-block:: sh

      $ http --form put :8084/projects/722de0eeb70011e69093fa163e5f2779/testsources/eaefe8b8b87911e69093fa163e5f2779 file@test.aic

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param testsource_id: identifier of the test source file
   :statuscode 204: the content has been updated


.. http:delete:: /projects/(string:project_id)

   Remove a project. Projects can only be removed if they don't contain running vms or campaigns.

   **Example request**:

   .. code-block:: sh

      $ http delete :8084/projects/3d7cff8eb6ff11e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 202 Accepted

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: the identifier of the project to remove
   :statuscode 202: the removal of the project has started
   :statuscode 404: the project does not exist, or the user cannot access it, or the user does not exist


.. http:delete:: /projects/(string:project_id)/apk/(string:apk_id)

   Delete an APK file from a project.

   **Example request**:

   .. code-block:: sh

      $ http delete :8084/projects/722de0eeb70011e69093fa163e5f2779/apk/282831ecb71011e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param apk_id: the APK file to remove
   :statuscode 204: the APK file has been deleted


.. http:delete:: /projects/(string:project_id)/camera/(string:camera_file_id)

   Delete a camera file from a project.

   **Example request**:

   .. code-block:: sh

      $ http delete :8084/projects/722de0eeb70011e69093fa163e5f2779/camera/15a56ea8b87911e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param camera_file_id: the camera file to remove
   :statuscode 204: the camera file has been deleted


.. http:delete:: /projects/(string:project_id)/testsources/(string:testsource_id)

   Delete a test source from a project.

   **Example request**:

   .. code-block:: sh

      $ http delete :8084/projects/722de0eeb70011e69093fa163e5f2779/testsources/eaefe8b8b87911e69093fa163e5f2779

   **Example response**:

   .. code-block:: http

      HTTP/1.1 204 No Content
      Content-Length: 0
      Content-Type: application/octet-stream

   :requestheader X-Auth-UserId: a user who has access to the project
   :param project_id: uuid of the project
   :param testsource_id: the test source to remove
   :statuscode 204: the test source has been deleted


.. http:get:: /user/quota

   Quota consumption and limits for the current user.

   **Example request**:

   .. code-block:: sh

      $ http :8084/user/quota

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "quota": {
              "vm_async_current": 0,
              "vm_async_max": 3,
              "vm_live_current": 0,
              "vm_live_max": 3
          }
      }

   :requestheader X-Auth-UserId: a user who needs to know its quota consumption
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json integer vm_async_current: current total of vms running a test campaign
   :>json integer vm_async_max: maximum number of concurrent vms in test campaigns
   :>json integer vm_live_current: current total of live vms for the user
   :>json integer vm_live_max: maximum number of concurrent live vms


.. http:get:: /user/whoami

   Information about the current user. Currently only the user id, which
   a frontend may not know if it authenticates with an opaque token.

   **Example request**:

   .. code-block:: sh

      $ http :8084/user/whoami

   **Example response**:

   .. code-block:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
          "user": {
              "userid": "marco"
          }
      }

   :requestheader X-Auth-UserId: a user
   :statuscode 200: no error
   :resheader Content-Type: always application/json
   :>json string userid: the unique user identifier


