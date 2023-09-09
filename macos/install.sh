#!/bin/bash

# TODO: add install check
softwareupdate --install-rosetta

brew update

brew install git-lfs
git lfs install --system

brew install qemu
# minikube start --driver=qemu
#brew install minikube
#brew install docker
#brew install docker-compose

#install docker-credential-helper

brew install --cask visual-studio-code
brew install --cask miniconda
brew install tmux
brew install jq
brew install nmap
brew install iterm2
brew install neovim

brew install watch
brew install stats
brew install watchexec


git config --global push.autoSetupRemote true


#!/bin/bash

mkdir -p ~/opt/dotnet

# install multiple .net versions

if [ ! -f ~/opt/dotnet/dotnet-install.sh ]; then
	curl -L -o ~/opt/dotnet/dotnet-install.sh https://dotnet.microsoft.com/download/dotnet/scripts/v1/dotnet-install.sh
	chmod +x ~/opt/dotnet/dotnet-install.sh
fi 
if [ ! -d ~/opt/dotnet/6.0.413 ]; then
    ~/opt/dotnet/dotnet-install.sh -i ~/opt/dotnet/6.0.413 -v 6.0.413
fi
if [ ! -d ~/opt/dotnet/7.0.400 ]; then
    ~/opt/dotnet/dotnet-install.sh -i ~/opt/dotnet/7.0.400 -v 7.0.400
fi

