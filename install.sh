#!/bin/bash


USERNAME=$USER
PROGRAM_NAME=$PassMan-NIX

exist() {
  if [ $(getent group) ]; then
    echo "group exists."
  else
    echo "group does not exist."
  fi

}

read -rs PASSWORD

echo "$PASSWORD" | sudo -S ls > /dev/null 2>&1
EXITCODE=$?

if [ $EXITCODE -ne 0 ]; then
    echo "Root Password is incorrect Try again!"
    exit 1
fi

echo "$PASSWORD" | sudo groupadd PassMan-NIX
echo "$PASSWORD" | sudo useradd -MU PassMan-NIX
echo "$PASSWORD" | sudo usermod -aG PassMan-NIX PassMan-NIX
