
Kyaraben client
===============

With the provided client, you can create, list and delete Android VMs (in
short, AVM) and the related services (display, debug bridge etc.)

.. program-output:: kyaraben help
   :prompt:

Most of of these commands provide a list or table output of some sorts; you can
easily change the output to JSON, comma-separated-values or other formats
supported by the `Cliff <http://docs.openstack.org/developer/cliff/>`_ package:

.. program-output:: kyaraben help android list
   :ellipsis: 0,15

Typing :command:`kyaraben` without any option provides an interactive console in which you
can run further subcommands and call an external editor.
Read `Cliff Interactive Mode <http://docs.openstack.org/developer/cliff/interactive_mode.html>`_
for more information.

All of the client commands are implemented through REST APIs; you can log the calls behind each
command with the *--debug-requests* option:

.. code-block:: sh

  $ kyaraben user whoami --debug-requests
  2016-11-28 10:51:58,014 INFO Starting new HTTP connection (1): 127.0.0.1
  Starting new HTTP connection (1): 127.0.0.1
  2016-11-28 10:51:58,018 DEBUG "GET /user/whoami HTTP/1.1" 200 29
  +--------+-------+
  | Field  | Value |
  +--------+-------+
  | userid | marco |
  +--------+-------+



Projects
--------

Resources (virtual machines, applications and assets) are organized in projects.
Creating a project is therefore the first step to consume most of the APIs.


Create / show a project
^^^^^^^^^^^^^^^^^^^^^^^

.. program-output:: kyaraben help project create
   :prompt:
   :ellipsis: -4

Example:

.. code-block:: sh

  $ kyaraben project create foobar
  e88a9326b19d11e690b1fa163e64e706

All log lines are sent to stderr, so it's easy to capture stdout and compose scripts:

.. code-block:: sh

  $ project_id=$(kyaraben project create foobar --verbose)
  Configuration file: kyaraben-client.ini
  Requesting project creation...
  Project created: 088f6ca0b19e11e690b1fa163e64e706
  $ echo $project_id
  088f6ca0b19e11e690b1fa163e64e706


You can retrieve data about the new project.

.. code-block:: sh

  $ kyaraben project show 088f6ca0b19e11e690b1fa163e64e706
  +-----------------+----------------------------------+
  | Field           | Value                            |
  +-----------------+----------------------------------+
  | count_avms      | 0                                |
  | project_id      | 088f6ca0b19e11e690b1fa163e64e706 |
  | project_name    | foobar                           |
  | status          | READY                            |
  | status_reason   |                                  |
  | status_ts       | 2016-11-23T17:05:18Z             |
  | sum_avms_uptime | 0.0                              |
  +-----------------+----------------------------------+

or in a more compact form:

.. code-block:: sh

  $ kyaraben project show 088f6ca0b19e11e690b1fa163e64e706 -f shell
  count_avms="0"
  project_id="020c4e92b19f11e690b1fa163e64e706"
  project_name="baz"
  status="READY"
  status_reason=""
  status_ts="2016-11-23T17:05:18Z"
  sum_avms_uptime="0.0"


The project's name can be changed after the creation:

.. code-block:: sh

  $ project_id=$(kyaraben project create foobar)
  $ kyaraben project update --project-name baz $project_id
  $ kyaraben project show $project_id
  +-----------------+----------------------------------+
  | Field           | Value                            |
  +-----------------+----------------------------------+
  | count_avms      | 0                                |
  | project_id      | 020c4e92b19f11e690b1fa163e64e706 |
  | project_name    | baz                              |
  | status          | READY                            |
  [...]



List / delete projects
^^^^^^^^^^^^^^^^^^^^^^

To show all the projects:

.. code-block:: sh

   $ kyaraben project list
   +----------------------------------+--------------+--------+
   | project_id                       | project_name | status |
   +----------------------------------+--------------+--------+
   | f6f326c2b31311e6a436fa163e316d19 | foobar       | READY  |
   | f975b6eeb31311e6a436fa163e316d19 | drwho        | READY  |
   | 0a915bc2b31411e6a436fa163e316d19 | panda        | READY  |
   +----------------------------------+--------------+--------+

To delete, pass the project id:

.. code-block:: sh

   $ kyaraben project delete f6f326c2b31311e6a436fa163e316d19 --verbose
   Deleted f6f326c2b31311e6a436fa163e316d19


Project ownership
^^^^^^^^^^^^^^^^^

A project is *owned* by the user who created it.

Users cannot create VMs, use them or upload files in a project they don't own (there
is a simple sharing mechanism but is unfinished).

By default, the :command:`kyaraben` command connects as the user defined in the file
:file:`kyaraben-client.ini`.

Since the requests to the kyaraben server are authorized through a separate component,
it is possible to impersonate other users:

.. code-block:: sh

  $ kyaraben project create drwho --as-user marco
  fb651ee0b31d11e6a436fa163e316d19
  $ kyaraben project create panda --as-user karine
  012381fab31e11e6a436fa163e316d19
  $ kyaraben project list --as-user karine
  +----------------------------------+--------------+--------+
  | project_id                       | project_name | status |
  +----------------------------------+--------------+--------+
  | 012381fab31e11e6a436fa163e316d19 | panda        | READY  |
  +----------------------------------+--------------+--------+
  $ kyaraben project list --as-user marco
  +----------------------------------+--------------+--------+
  | project_id                       | project_name | status |
  +----------------------------------+--------------+--------+
  | fb651ee0b31d11e6a436fa163e316d19 | drwho        | READY  |
  +----------------------------------+--------------+--------+

Likewise, most other subcommands accept the *--as-user* parameter.


Android Images
--------------

Android images are used to instantiate AVMs. At the moment, only the *list*
API is available. The data is stored in the SQL table "images".

.. code-block:: sh

  $ kyaraben image list
  +-----------------+-----------------+
  | android_version | image           |
  +-----------------+-----------------+
  |               4 | kitkat-tablet   |
  |               4 | kitkat-phone    |
  |               5 | lollipop-tablet |
  |               5 | lollipop-phone  |
  +-----------------+-----------------+


.. note::

  Creating a VM with the AiC image *kitkat-tablet* would actually look up in the SQL database
  for the real image names to use (in this case, by default, *system-kitkat-tablet*
  and *data-kitkat-tablet*).
  The fact the AVM is using two partitions (three with the sdcard) is transparent to AiC users,
  and only referenced in the Heat template.



Android VMs
-----------

Create / delete VMs
^^^^^^^^^^^^^^^^^^^

The *android create* subcommand accepts a few parameters.

.. program-output:: kyaraben help android create
   :prompt:


Only the project_id and the image name are required, but a name for the vm can be specified:

.. code-block:: sh

  $ project_id=f975b6eeb31311e6a436fa163e316d19
  $ kyaraben android create $project_id --image kitkat-tablet --avm-name poyo
  4f500c52b31b11e6a436fa163e316d19

The remaining parameters relate to the emulated hardware environment (screen size,
presence of sensors or devices).

.. code-block:: sh

  $ kyaraben android create f975b6eeb31311e6a436fa163e316d19 --image kitkat-tablet --width 1280 \
  --height 800 --dpi 240
  7ca58e6cb32911e6a436fa163e316d19


To delete a VM, the project_id is not required:

.. code-block:: sh

  $ kyaraben android delete 7ca58e6cb32911e6a436fa163e316d19 --verbose
  Deleted 7ca58e6cb32911e6a436fa163e316d19


Like for projects, the vm's name can be changed after the creation.

.. code-block:: sh

  $ kyaraben android update 4f500c52b31b11e6a436fa163e316d19 --avm-name foobar
  $ kyaraben android show 4f500c52b31b11e6a436fa163e316d19 -f value -c avm_name
  foobar




Retrieve AVM data
^^^^^^^^^^^^^^^^^

After a VM has been created, its status becomes READY and it's possible to retrieve
its metadata:

.. code-block:: sh

  $  kyaraben android show 4f500c52b31b11e6a436fa163e316d19 -f shell
  avm_id="4f500c52b31b11e6a436fa163e316d19"
  avm_name="foobar"
  avm_owner="karine"
  campaign_id=""
  hwconfig="{'height': 600, 'enable_camera': 1, 'enable_gsm': 1, 'enable_sensors': 1, 'enable_battery': 1,
  'enable_nfc': 0, 'dpi': 160, 'enable_gps': 1, 'enable_record': 0, 'width': 800}"
  image="kitkat-tablet"
  project_id="f975b6eeb31311e6a436fa163e316d19"
  status="READY"
  status_reason=""
  status_ts="2016-11-25T14:28:41Z"
  ts_created="2016-11-25T14:27:35Z"
  uptime="4930.114172"


The VMs can be listed with or without filtering by project_id:

.. code-block:: sh

  $ kyaraben android list
  +-----------------+----------+-----------+-------------+-----------------+-----------------+...
  | avm_id          | avm_name | avm_owner | campaign_id | image           | project_id      |
  +-----------------+----------+-----------+-------------+-----------------+-----------------+...
  | 33cad8d6b32a11e | 33cad8d6 | karine    |             | lollipop-tablet | f975b6eeb31311e |
  | 6a436fa163e316d |          |           |             |                 | 6a436fa163e316d |
  | 19              |          |           |             |                 | 19              |
  | 2c5b3b4ab32a11e | 2c5b3b4a | karine    |             | lollipop-phone  | f975b6eeb31311e |
  | 6a436fa163e316d |          |           |             |                 | 6a436fa163e316d |
  | 19              |          |           |             |                 | 19              |
  | 31136fb8b32a11e | 31136fb8 | karine    |             | kitkat-tablet   | 0a915bc2b31411e |
  | 6a436fa163e316d |          |           |             |                 | 6a436fa163e316d |
  | 19              |          |           |             |                 | 19              |
  +-----------------+----------+-----------+-------------+-----------------+-----------------+...
  $ kyaraben android list --project 0a915bc2b31411e6a436fa163e316d19
  +-----------------+----------+-----------+-------------+---------------+-----------------+--...
  | avm_id          | avm_name | avm_owner | campaign_id | image         | project_id      |
  +-----------------+----------+-----------+-------------+---------------+-----------------+--...
  | 31136fb8b32a11e | 31136fb8 | karine    |             | kitkat-tablet | 0a915bc2b31411e |
  | 6a436fa163e316d |          |           |             |               | 6a436fa163e316d |
  | 19              |          |           |             |               | 19              |
  +-----------------+----------+-----------+-------------+---------------+-----------------+--...


The state of Android system properties can be retrieved when the VM is operational:

.. code-block:: sh

  $ kyaraben android properties cb19a022b54c11e6a436fa163e316d19
  +--------------------------------+-------------------------------------------------------------------------------+
  | Field                          | Value                                                                         |
  +--------------------------------+-------------------------------------------------------------------------------+
  [...]
  | aicd.orientation.azimuth       | 0.000000                                                                      |
  | aicd.orientation.pitch         | 0.000000                                                                      |
  | aicd.orientation.roll          | 0.000000                                                                      |
  | aicd.screen_rotation           | 0                                                                             |
  | aicd.telemeter.distance        | 8.000000                                                                      |
  | aicd.thermometer.temperature   | 9.000000                                                                      |
  | dalvik.vm.heapsize             | 256m                                                                          |
  | dalvik.vm.stack-trace-file     | /data/anr/traces.txt                                                          |
  | debug.force_rtl                | 0                                                                             |
  | dev.bootcomplete               | 1                                                                             |
  | dhcp.eth1.dns1                 | 8.8.4.4                                                                       |
  | dhcp.eth1.dns2                 | 8.8.8.8                                                                       |
  | dhcp.eth1.dns3                 |                                                                               |
  | dhcp.eth1.dns4                 |                                                                               |
  | dhcp.eth1.domain               | openstacklocal                                                                |
  [...]
  | service.bootanim.exit          | 1                                                                             |
  | sys.boot_completed             | 1                                                                             |
  | sys.settings_global_version    | 3                                                                             |
  | sys.settings_secure_version    | 9                                                                             |
  | sys.settings_system_version    | 7                                                                             |
  | sys.sysctl.extra_free_kbytes   | 5625                                                                          |
  | sys.sysctl.tcp_def_init_rwnd   | 60                                                                            |
  | sys.usb.config                 | adb                                                                           |
  | sys.usb.state                  | adb                                                                           |
  | wifi.interface                 | eth1                                                                          |
  | wifi.interface.mac             | fa:16:3e:85:42:27                                                             |
  | wlan.driver.status             | ok                                                                            |
  +--------------------------------+-------------------------------------------------------------------------------+


Generate connection password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The VM screen output is authenticated with a *one-time password*, which must be used
to open an HTTP connection within 30 seconds. A password can be requested at any time.

.. code-block:: sh

  $ avm_id=cf7c92e0dbf911e690e6fa163e15ccce
  $ kyaraben android otp $avm_id
  378494



Retrieve status of asynchronous commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some of the APIs return a *command_id* value, which can be used to track the status
of the ongoing operation.

.. code-block:: sh

  $ avm_id=d1d9b7f2dbf911e690e6fa163e15ccce
  $ command_id=7f8a02e4dbfa11e690e6fa163e15ccce
  $ kyaraben android command status $avm_id $command_id
  +------------+-----------------------------------------------------------+
  | Field      | Value                                                     |
  +------------+-----------------------------------------------------------+
  | returncode | 0                                                         |
  | status     | READY                                                     |
  | stderr     | 7202 KB/s (2853346 bytes in 0.386s)                       |
  | stdout     | pkg: /data/local/tmp/66b95e0edbfa11e690e6fa163e15ccce.apk |
  |            | Success                                                   |
  +------------+-----------------------------------------------------------+


APKs
----

APK is the package file format for Android applications. An APK file is stored in a project
and can be deployed to any VM in the same project.


Upload / manage APKs in a project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have not built any APK file yourself, you can find some open source ones on https://f-droid.org:

.. code-block:: sh

  $ wget https://f-droid.org/repo/com.uberspot.a2048_23.apk
  [...]
  $ kyaraben project apk upload 0a915bc2b31411e6a436fa163e316d19 com.uberspot.a2048_23.apk
  Uploading com.uberspot.a2048_23.apk
  3f588992b55411e6a436fa163e316d19

When a file is uploaded, it is assigned a unique apk_id - there is no control on duplicate file names
on the server.

The files can then be listed and deleted. The *package* value can be used in the *android apk list* command
or in the monkey tests.

.. code-block:: sh

  $ project_id=0a915bc2b31411e6a436fa163e316d19
  $ apk_id=3f588992b55411e6a436fa163e316d19
  $ kyaraben project apk list $project_id -f yaml
  - apk_id: 3f588992b55411e6a436fa163e316d19
    filename: com.uberspot.a2048_23.apk
    package: com.uberspot.a2048
    project_id: 0a915bc2b31411e6a436fa163e316d19
    status: READY
  $ kyaraben project apk show $project_id $apk_id -f yaml
  apk_id: 3f588992b55411e6a436fa163e316d19
  filename: com.uberspot.a2048_23.apk
  package: com.uberspot.a2048
  project_id: 0a915bc2b31411e6a436fa163e316d19
  status: READY
  status_reason: ''
  $ kyaraben project apk delete $project_id $apk_id
  Deleted 3f588992b55411e6a436fa163e316d19



Install / list APKs in a VM
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once an APK is uploaded to a project, it can be installed.
Installing APK is an asynchronous operation, but you can track the status of the install command, and
see possible errors.

.. code-block:: sh

  $ avm_id=f40d2ec4b55911e6a436fa163e316d19
  $ apk_id=3f588992b55411e6a436fa163e316d19
  Install requested: 3f588992b55411e6a436fa163e316d19 on f40d2ec4b55911e6a436fa163e316d19.
  To know if the installation is successful, run "kyaraben android command status f40d2ec4b55911e6a436fa163e316d19 8707f254b55a11e6a436fa163e316d19"
  8707f254b55a11e6a436fa163e316d19
  $ command_id=8707f254b55a11e6a436fa163e316d19
  $ kyaraben android command status $avm_id $command_id
  +------------+-----------------------------------------------------------+
  | Field      | Value                                                     |
  +------------+-----------------------------------------------------------+
  | returncode | 0                                                         |
  | status     | READY                                                     |
  | stderr     | 4399 KB/s (872273 bytes in 0.193s)                        |
  | stdout     | pkg: /data/local/tmp/3f588992b55411e6a436fa163e316d19.apk |
  |            | Success                                                   |
  +------------+-----------------------------------------------------------+

There is also a *list* command, but it shows the installed APKs as *packages* rather than *files*:

.. code-block:: sh

  $ kyaraben android apk list f40d2ec4b55911e6a436fa163e316d19
  +-----------------------------+
  | package                     |
  +-----------------------------+
  | com.uberspot.a2048          |
  | com.example.android.apis    |
  | com.android.gesture.builder |
  +-----------------------------+


Camera emulation
----------------

The emulator can present a virtual camera image (or movie) to the applications.
Like with APKs, camera files need to be upload to the project, and activated for each VM.
A file can be an image or video, it will be converted if necessary.

.. code-block:: sh

  $ project_id=fb651ee0b31d11e6a436fa163e316d19
  $ kyaraben project camera upload $project_id zebre.mpg
  Uploading zebre.mpg
  3cf46284b56811e6a436fa163e316d19

Listing and deleting camera files is similar:

.. code-block:: sh

  $ kyaraben project camera list $project_id
  +----------------------------------+-----------+----------------------------------+--------+
  | camera_id                        | filename  | project_id                       | status |
  +----------------------------------+-----------+----------------------------------+--------+
  | 3cf46284b56811e6a436fa163e316d19 | zebre.mpg | fb651ee0b31d11e6a436fa163e316d19 | READY  |
  +----------------------------------+-----------+----------------------------------+--------+
  $ kyaraben project camera delete $project_id $camera_id
  Deleted 3cf46284b56811e6a436fa163e316d19




Instrumented Tests
------------------

There are two types of APKs: regular applications and `Instrumented Tests <https://developer.android.com/studio/test/index.html>`_.

To execute a test, Android loads a *Test APK* and a *Debug APK* (the app under test) together, in the same process.

The Test APK can be uploaded in the same way as the Debug APK, but AiC also provides a compiler-as-a-service,
implementing a DSL syntax.



Test sources: create / list / delete / compile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A test source can be uploaded and updated:


.. code-block:: sh

  $ project_id=fb651ee0b31d11e6a436fa163e316d19
  $ kyaraben project testsource create $project_id test.aic
  Uploading test.aic
  6c205cacb57711e6a436fa163e316d19
  [...]
  $ kyaraben project testsource update $project_id 6c205cacb57711e6a436fa163e316d19 test.aic
  Updating test.aic


Once uploaded, the tests can be listed or downloaded.

.. code-block:: sh

  $ kyaraben project testsource list $project_id
  +--------+----------+----------------------------------+--------+----------------------------------+
  | apk_id | filename | project_id                       | status | testsource_id                    |
  +--------+----------+----------------------------------+--------+----------------------------------+
  |        | test.aic | fb651ee0b31d11e6a436fa163e316d19 | READY  | 6c205cacb57711e6a436fa163e316d19 |
  +--------+----------+----------------------------------+--------+----------------------------------+
  $ kyaraben project testsource download $project_id 6c205cacb57711e6a436fa163e316d19
  Feature: "Best feature ever"
     Scenario: "Best scenario ever"
  [...]


The value *apk_id* refers to the APK that will be generated upon compiling.

Compilation takes some time, but the API call returns immediately:

.. code-block:: sh

  $ kyaraben project testsource compile $project_id 6c205cacb57711e6a436fa163e316d19
  Compiling APK 8f5deaf8b57811e6a436fa163e316d19
  8f5deaf8b57811e6a436fa163e316d19

The return value is an apk_id -- though the APK is still not ready:

.. code-block:: sh

  $ kyaraben project apk show $project_id 8f5deaf8b57811e6a436fa163e316d19
  +---------------+----------------------------------+
  | Field         | Value                            |
  +---------------+----------------------------------+
  | apk_id        | 8f5deaf8b57811e6a436fa163e316d19 |
  | filename      | test.apk                         |
  | package       |                                  |
  | project_id    | fb651ee0b31d11e6a436fa163e316d19 |
  | status        | COMPILING DSL                    |
  | status_reason |                                  |
  +---------------+----------------------------------+

When status is READY, it becomes possible to install the APK or use it in a test campaign.

If there is any compilation error, the status becomes ERROR and a detailed log is reported as status_reason.

For convenience, these errors and apk_status are also reported in the *testsource show* command:

.. code-block:: sh

  $ kyaraben project testsource show $project_id 6c205cacb57711e6a436fa163e316d19
  +-------------------+----------------------------------+
  | Field             | Value                            |
  +-------------------+----------------------------------+
  | apk_id            | 8f5deaf8b57811e6a436fa163e316d19 |
  | apk_status        | READY                            |
  | apk_status_reason |                                  |
  | filename          | test.aic                         |
  | project_id        | fb651ee0b31d11e6a436fa163e316d19 |
  | status            | READY                            |
  | testsource_id     | 6c205cacb57711e6a436fa163e316d19 |
  +-------------------+----------------------------------+

Deleting a testsource does not automatically delete the compiled APK:

.. code-block:: sh

  $ kyaraben project testsource delete $project_id 6c205cacb57711e6a436fa163e316d19
  Deleted 6c205cacb57711e6a436fa163e316d19
  $ kyaraben project testsource show $project_id 6c205cacb57711e6a436fa163e316d19
  Testsource '6c205cacb57711e6a436fa163e316d19' not found
  404 Client Error: Not Found for url: http://127.0.0.1:8084/projects/fb651ee0b31d11e6a436fa163e316d19/testsources/6c205cacb57711e6a436fa163e316d19/metadata
  $ kyaraben project apk show $project_id 8f5deaf8b57811e6a436fa163e316d19
  +---------------+----------------------------------+
  | Field         | Value                            |
  +---------------+----------------------------------+
  | apk_id        | 8f5deaf8b57811e6a436fa163e316d19 |
  | filename      | test.apk                         |
  | package       |                                  |
  | project_id    | fb651ee0b31d11e6a436fa163e316d19 |
  | status        | READY                            |
  | status_reason |                                  |
  +---------------+----------------------------------+
  $ kyaraben project apk delete $project_id 8f5deaf8b57811e6a436fa163e316d19
  Deleted 8f5deaf8b57811e6a436fa163e316d19


Running test APKs
^^^^^^^^^^^^^^^^^

Once a test APK is installed, it provides test packages:

.. code-block:: sh

  $ avm_id=d1d9b7f2dbf911e690e6fa163e15ccce
  $ kyaraben android test list $avm_id
  +--------------------------------------------------------------------------------+-------------------------------+
  | package                                                                        | target                        |
  +--------------------------------------------------------------------------------+-------------------------------+
  | com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner           | com.zenika.aic.core.libs.test |
  | com.zenika.aic.demo.sensor.test/android.support.test.runner.AndroidJUnitRunner | com.zenika.aic.demo.sensor    |
  +--------------------------------------------------------------------------------+-------------------------------+


These test packages can be run outside of test campaigns, on specific VM instances:

.. code-block:: sh

  $ kyaraben android test run $avm_id com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner
  To retrieve the result, run "kyaraben android command status d1d9b7f2dbf911e690e6fa163e15ccce 1dd905e4dbfb11e690e6fa163e15ccce"
  1dd905e4dbfb11e690e6fa163e15ccce


Since the test can take a while to run, the output is stored and can be retrieved with a command_id:

.. code-block:: sh

  $ command_id=caeffefedbfb11e690e6fa163e15ccce
  $ kyaraben android command status $avm_id $command_id
  +------------+-------------------------------------------------------------------+
  | Field      | Value                                                             |
  +------------+-------------------------------------------------------------------+
  | returncode | 0                                                                 |
  | status     | READY                                                             |
  | stderr     |                                                                   |
  | stdout     | INSTRUMENTATION_STATUS: numtests=2                                |
  |            | INSTRUMENTATION_STATUS: stream=                                   |
  |            | com.zenika.aic.core.libs.ParserTest:                              |
  |            | INSTRUMENTATION_STATUS: id=InstrumentationTestRunner              |
  |            | INSTRUMENTATION_STATUS: test=testAndroidTestCaseSetupProperly     |
  |            | INSTRUMENTATION_STATUS: class=com.zenika.aic.core.libs.ParserTest |
  [...]


Test campaigns
^^^^^^^^^^^^^^

Test runs can be grouped in a *Test Campaign*. With a test campaign, the same test APK
can be run in multiple VM configurations, or the same VM configuration can be used to
run several test APKs. How many test runs are actually executed at any one time is
defined by the *async user quota*.

To define and run a test campaign:

.. code-block:: sh

  $ kyaraben project campaign run 63f49082dbf811e690e6fa163e15ccce --image kitkat-tablet --image lollipop-phone --package com.zenika.aic.demo.sensor.test/android.support.test.runner.AndroidJUnitRunner --package com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner --apk 54cf0536dbfa11e690e6fa163e15ccce --apk 4f541b82dbfa11e690e6fa163e15ccce
  Test campaign requested: {'tests': [{'packages': ['com.zenika.aic.demo.sensor.test/android.support.test.runner.AndroidJUnitRunner', 'com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner'], 'apks': ['54cf0536dbfa11e690e6fa163e15ccce', '4f541b82dbfa11e690e6fa163e15ccce'], 'image': 'kitkat-tablet'}, {'packages': ['com.zenika.aic.demo.sensor.test/android.support.test.runner.AndroidJUnitRunner', 'com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner'], 'apks': ['54cf0536dbfa11e690e6fa163e15ccce', '4f541b82dbfa11e690e6fa163e15ccce'], 'image': 'lollipop-phone'}]}.
  8bbe5d58dc0411e690e6fa163e15ccce


For each of the listed images, all of the apks will be installed, and all of
the listed packages will be executed. The corresponding REST API provides a finer control
over the list of tests to run for each image and the hardware configuration of each VM.


To retrieve the execution state and test results of a campaign:

.. code-block:: sh

  $ project_id=63f49082dbf811e690e6fa163e15ccce
  $ campaign_id=8bbe5d58dc0411e690e6fa163e15ccce
  $ kyaraben project campaign show $poject_id $campaign_id
  +-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | Field           | Value                                                                                                                                                                    |
  +-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
  | campaign_id     | 8bbe5d58dc0411e690e6fa163e15ccce                                                                                                                                         |
  | campaign_name   | lovely-big-cobra                                                                                                                                                         |
  | campaign_status | RUNNING                                                                                                                                                                  |
  | progress        | 0.0                                                                                                                                                                      |
  | project_id      | 63f49082dbf811e690e6fa163e15ccce                                                                                                                                         |
  | tests           | [{'hwconfig': {'enable_camera': 1, 'enable_gsm': 1, 'enable_gps': 1, 'enable_nfc': 0, 'enable_record': 0, 'height': 600, 'enable_battery': 1, 'enable_sensors': 1,       |
  |                 | 'width': 800, 'dpi': 160}, 'status': 'QUEUED', 'stdout': '', 'package': 'com.zenika.aic.demo.sensor.test/android.support.test.runner.AndroidJUnitRunner', 'image':       |
  |                 | 'kitkat-tablet'}, {'hwconfig': {'enable_camera': 1, 'enable_gsm': 1, 'enable_gps': 1, 'enable_nfc': 0, 'enable_record': 0, 'height': 600, 'enable_battery': 1,           |
  |                 | 'enable_sensors': 1, 'width': 800, 'dpi': 160}, 'status': 'QUEUED', 'stdout': '', 'package': 'com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner',     |
  |                 | 'image': 'kitkat-tablet'}, {'hwconfig': {'enable_camera': 1, 'enable_gsm': 1, 'enable_gps': 1, 'enable_nfc': 0, 'enable_record': 0, 'height': 600, 'enable_battery': 1,  |
  |                 | 'enable_sensors': 1, 'width': 800, 'dpi': 160}, 'status': 'QUEUED', 'stdout': '', 'package':                                                                             |
  |                 | 'com.zenika.aic.demo.sensor.test/android.support.test.runner.AndroidJUnitRunner', 'image': 'lollipop-phone'}, {'hwconfig': {'enable_camera': 1, 'enable_gsm': 1,         |
  |                 | 'enable_gps': 1, 'enable_nfc': 0, 'enable_record': 0, 'height': 600, 'enable_battery': 1, 'enable_sensors': 1, 'width': 800, 'dpi': 160}, 'status': 'QUEUED', 'stdout':  |
  |                 | '', 'package': 'com.zenika.aic.core.libs.test/android.test.InstrumentationTestRunner', 'image': 'lollipop-phone'}]                                                       |
  +-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+



Test campaigns can also be listed or deleted:

.. code-block:: sh

  $ kyaraben project campaign list $project_id
  +----------------------------------+-------------------+----------------------------------+---------+
  | campaign_id                      | campaign_name     | project_id                       | status  |
  +----------------------------------+-------------------+----------------------------------+---------+
  | 7ca2c674dc0411e690e6fa163e15ccce | newly-happy-burro | 63f49082dbf811e690e6fa163e15ccce | RUNNING |
  | 8bbe5d58dc0411e690e6fa163e15ccce | lovely-big-cobra  | 63f49082dbf811e690e6fa163e15ccce | RUNNING |
  +----------------------------------+-------------------+----------------------------------+---------+
  $ kyaraben project campaign delete 63f49082dbf811e690e6fa163e15ccce 7ca2c674dc0411e690e6fa163e15ccce
  Deleted 7ca2c674dc0411e690e6fa163e15ccce


Monkey tests
^^^^^^^^^^^^

The `UI/Application Exerciser Monkey <https://developer.android.com/studio/test/monkey.html>`_
can be run on a test package:

.. code-block:: sh

  $ avm_id=cf7c92e0dbf911e690e6fa163e15ccce
  $ kyaraben android monkey run $avm_id --package com.zenika.aic.demo.sensor.test/android.support.test.runner.AndroidJUnitRunner --throttle 1 1000
  To retrieve the result, run "kyaraben android command status cf7c92e0dbf911e690e6fa163e15ccce 76ec6df0dc0b11e690e7fa163e15ccce"
  76ec6df0dc0b11e690e7fa163e15ccce



User information
----------------

A user may need to know its user id, especially after authenticating with an opaque token:

.. code-block:: sh

  $ kyaraben user whoami
  +--------+-------+
  | Field  | Value |
  +--------+-------+
  | userid | marco |
  +--------+-------+


More importantly, the user can ask for the current quota limits:

.. code-block:: sh

  $ kyaraben user quota
  +------------------+-------+
  | Field            | Value |
  +------------------+-------+
  | vm_async_current | 0     |
  | vm_async_max     | 3     |
  | vm_live_current  | 2     |
  | vm_live_max      | 3     |
  +------------------+-------+

