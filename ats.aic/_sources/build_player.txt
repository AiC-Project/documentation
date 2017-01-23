
Building the Player
===================

On the controller, download the sources for the AiC Player containers:


.. code-block:: sh

  (controller)developer@dev-controller:~/aic$ aic player source
  Cloning Player.
  Cloning into '/data/home/developer/aic/src/player'...
  [...]
  Checking connectivity... done.
  Clone complete.


Build both the binaries and the Docker images:


.. code-block:: sh

  (controller)developer@dev-controller:~/aic$ aic player build
  Building Player binaries + images.
  [...]
   ---> Running in 07fd23f13e60
   ---> c5f708cb7a68
  Removing intermediate container 07fd23f13e60
  Successfully built c5f708cb7a68
  Saving docker images...
  Build complete in /data/home/developer/aic/images/docker-images.tar
 
