
Building the frontend
=====================

On the controller, download the sources for the web frontend:


.. code-block:: sh

  (controller) developer@dev-controller:~/aic$ aic frontend source
  Cloning frontend.
  Cloning into '/data/home/developer/aic/src/frontend'...
  remote: Counting objects: 6214, done.
  [...]
  Checking connectivity... done.
  Clone complete.


Build the frontend package:


.. code-block:: sh

  (controller) developer@dev-controller:~/aic$ aic frontend build
  Building frontend.
  front-end-app@0.7.1 /data/home/developer/aic/src/frontend
  ├── attr-accept@1.0.3
  ├─┬ babel-cli@6.11.4
  [...]

  Hash: 4b258b3b2c1c8173ebeb
  Version: webpack 2.1.0-beta.21
  Time: 107558ms
   Asset     Size  Chunks             Chunk Names
  app.js  1.31 MB       0  [emitted]  main
      + 785 hidden modules
  Build complete in /data/home/developer/aic/images/frontend.tgz

