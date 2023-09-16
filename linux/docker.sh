#!/bin/bash

sudo apt install -y curl uidmap
curl -fsSL https://get.docker.com -o get-docker.sh
#sudo sh ./get-docker.sh --dry-run
sudo sh ./get-docker.sh
dockerd-rootless-setuptool.sh install

# add to your exports file
# echo "export DOCKER_HOST=unix:///run/user/1000/docker.sock" >> ~/.bash_exports

rm get-docker.sh
