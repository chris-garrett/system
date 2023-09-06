#!/bin/bash

#bash minikube start
#eval $(minikube docker-env)

if [ -f ~/.docker/config.json ]; then
  echo "CONFIG EXISTS"
else
  echo "NO CONFIG"
  mkdir -p ~/.docker
  printf '{\n"credsStore" : "osxkeychain"\n}\n' > ~/.docker/config.json
fi
#~/.docker/config.json

minikube start --container-runtime=docker --vm=true

