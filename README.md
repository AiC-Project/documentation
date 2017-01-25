# AiC Documentation

This repository collects the AiC documentation.
It is also an example on how to integrate a project with Travis to
automatically build the documentation and publish it.

## How to include a new project to AiC documentation Github pages

For automated publishing you will need to create a deployment key with
write access.

To secure the key we encrypt it with travis client. You should follow
[Travis documentation on Encrypting files](https://docs.travis-ci.com/user/encrypting-files/).

Add the encrypted file to your repository (for example deploy_key.enc).
DO NOT add the original non encrypted key.

Add a .travis.yml file with the build and publish instructions.

You can check .travis/publish-docs.sh for a script that publishes the
documentation build result in a GitHub Pages branch. You need to set
several environment variables in Travis to use this script.

## References

[Auto-deploying built products to gh-pages with Travis](https://gist.github.com/domenic/ec8b0fc8ab45f39403dd)

[Generating a new SSH key and adding it to the ssh-agent](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)

[Auto-deploying Doxygen documentation to gh-pages with Travis CI](https://gist.github.com/vidavidorra/548ffbcdae99d752da02)
