#!/bin/bash

brew update

brew install git-lfs
git lfs install --system

brew install qemu
# minikube start --driver=qemu
brew install minikube
brew install docker
brew install docker-compose

install docker-credential-helper

brew install --cask visual-studio-code
brew install --cask miniconda
brew install tmux
brew install jq
brew install nmap


git config --global push.autoSetupRemote true
