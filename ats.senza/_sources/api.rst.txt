
API Reference
=============

For the examples, we'll use `Resty <https://github.com/micha/resty>`_

.. code-block:: console

    $ . resty
    $ resty http://127.0.0.1:8083
    http://127.0.0.1:8083*


Example response of a successful request:

.. sourcecode:: http

  HTTP/1.1 204 No Content
  CONTENT-LENGTH: 0
  CONNECTION: keep-alive
  DATE: Wed, 04 Nov 2015 10:32:40 GMT
  SERVER: Python/3.5 aiohttp/0.18.3



Accelerometer
-------------

.. http:post:: /android/sensors/accelerometer/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/accelerometer/jHLGWPeRSVyVzyCpWRsEjg \
      '{"x":"0","y":"0.5","z":"1.0"}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float x: orientation vector x
   :jsonparam float y: orientation vector y
   :jsonparam float z: orientation vector z
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Battery
-------

.. http:post:: /android/sensors/battery/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/battery/jHLGWPeRSVyVzyCpWRsEjg '{"level":40}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam int level: the battery level
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Camera
------

.. http:post:: /android/sensors/camera/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/camera/jHLGWPeRSVyVzyCpWRsEjg '{"file_id":"zebre.mpg"}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam string file_id: the name of the video file (or in the cloud version or AiC, the file id)
                              to be found under the folder $SENZA_CAMERA_VIDEO_PATH
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)



GPS
---

.. http:post:: /android/sensors/gps/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gps/jHLGWPeRSVyVzyCpWRsEjg \
      '{"latitude":48.8567,"longitude":2.3508}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float latitude: the latitude (+ is North, - is South)
   :jsonparam float longitude: the longitude (+ is East, - is West)
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Gravity
-------

.. http:post:: /android/sensors/gravity/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gravity/jHLGWPeRSVyVzyCpWRsEjg \
      '{"x": 0, "y": 9.776, "z": 0.813}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float x: gravity vector x
   :jsonparam float y: gravity vector y
   :jsonparam float z: gravity vector z
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

GSM
---

Call
~~~~

.. http:post:: /android/sensors/gsm/call/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gsm/call/jHLGWPeRSVyVzyCpWRsEjg \
      '{"action": "receive", "phone_number": "+3312345"}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam string action: Action type to perform (one of "accept", "cancel", "hold", "receive")
   :jsonparam string phone_number: The (remote) phone number used for the call action
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Network
~~~~~~~

.. http:post:: /android/sensors/gsm/network/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gsm/network/jHLGWPeRSVyVzyCpWRsEjg '{"type": "lte"}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam string type: The network type to use (one of "gsm", "gprs", "edge", "cdma", "hspa",
        "hsupa", "umts", "hsdpa", "evdo", "lte", "full")
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)


Registration
~~~~~~~~~~~~

.. http:post:: /android/sensors/gsm/registration/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gsm/registration/jHLGWPeRSVyVzyCpWRsEjg '{"type": "home"}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam string type: The gsm registration type to use (one of "home", "denied", "searching", "roaming", "none")
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)


Signal
~~~~~~

.. http:post:: /android/sensors/gsm/signal/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gsm/signal/jHLGWPeRSVyVzyCpWRsEjg '{"strength": 3}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam string strength: The sms strength (between 0, the minimum, and 4, the maximum)
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Sms
~~~

.. http:post:: /android/sensors/gsm/sms/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gsm/sms/jHLGWPeRSVyVzyCpWRsEjg \
      '{"phone_number": "+3312345", "text": "Bonjour"}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam string phone_number: The (remote) phone number the sms will be received from
   :jsonparam string text: The sms text to be received
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Gyroscope
---------

.. http:post:: /android/sensors/gyroscope/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/gyroscope/jHLGWPeRSVyVzyCpWRsEjg \
      '{"azimuth": 0, "pitch": 9.776, "roll": 0.813}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float azimuth: device azimuth in degrees
   :jsonparam float pitch: device pitch in degrees
   :jsonparam float roll: device roll in degrees
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Light
-----

.. http:post:: /android/sensors/light/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/light/jHLGWPeRSVyVzyCpWRsEjg '{"light": 90}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float pressure: light (in lux)
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Linear acceleration
-------------------

.. http:post:: /android/sensors/linear_acc/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/linear_acc/jHLGWPeRSVyVzyCpWRsEjg \
      '{"x": 0, "y": 9.776, "z": 0.813}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float x: linear acceleration vector x (in m/s²)
   :jsonparam float y: linear acceleration vector y (in m/s²)
   :jsonparam float z: linear acceleration vector z (in m/s²)
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Magnetometer
------------

.. http:post:: /android/sensors/magnetometer/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/magnetometer/jHLGWPeRSVyVzyCpWRsEjg \
      '{"x": 0, "y": 9.776, "z": 0.813}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float x: magnetometer vector x (in µT)
   :jsonparam float y: magnetometer vector y (in µT)
   :jsonparam float z: magnetometer vector z (in µT)
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Orientation
-----------

.. http:post:: /android/sensors/orientation/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/orientation/jHLGWPeRSVyVzyCpWRsEjg \
      '{"azimuth": 0, "pitch": 9.776, "roll": 0.813}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float azimuth: device azimuth in degrees
   :jsonparam float pitch: device pitch in degrees
   :jsonparam float roll: device roll in degrees
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Pressure
--------

.. http:post:: /android/sensors/pressure/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/pressure/jHLGWPeRSVyVzyCpWRsEjg '{"pressure": 100}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float pressure: pressure in hPa
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Proximity
---------

.. http:post:: /android/sensors/proximity/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/proximity/jHLGWPeRSVyVzyCpWRsEjg '{"distance": 50}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float proximity: proximity in cm
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)


Relative Humidity
-----------------

.. http:post:: /android/sensors/relative_humidity/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/relative_humidity/jHLGWPeRSVyVzyCpWRsEjg \
      '{"relative_humidity": 50}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float relative_humidity: relative humidity in %
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Rotation vector
---------------

.. http:post:: /android/sensors/rotation_vector/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/rotation_vector/jHLGWPeRSVyVzyCpWRsEjg \
      '{"x": 0, "y": 9.776, "z": 0.813, "angle": 12.783, "accuracy": 50}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam float x: rotation vector x
   :jsonparam float y: rotation vector y
   :jsonparam float z: rotation vector z
   :jsonparam float angle: rotation angle
   :jsonparam float accuracy: estimated accuracy (in radians)
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)


Temperature
-----------

.. http:post:: /android/sensors/temperature/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/temperature/jHLGWPeRSVyVzyCpWRsEjg '{"temperature": 18}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam temperature: temperature in celsius degrees
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

Recording
---------

.. http:post:: /android/sensors/recording/{avm_id}

   **Example request**:

   .. sourcecode:: console

      $ POST /android/sensors/recording/jHLGWPeRSVyVzyCpWRsEjg \
      '{"filename":"recording.avi","start":"1"}' -i

   :param avm_id: the virtual machine to which the data will be sent
   :jsonparam string filename: the filename to hold the video recording
   :jsonparam int start: whether to start or stop the recording (1 to start, 0 to stop)
   :statuscode 204: the data has been sent
   :statuscode 400: the data is not well formed (see response content)

