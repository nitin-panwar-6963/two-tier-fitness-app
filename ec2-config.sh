#!/bin/bash

#---------------------------------update-----------------------------------

echo "Updating system..."

sudo apt update -y
sudo apt upgrade -y

echo "Successfully updated ......"

#---------------------------------docker-----------------------------------

echo "Starting Docker installation..."

sudo apt install docker.io -y

sudo systemctl start docker
sudo systemctl enable docker

echo "Docker started successfully ...."

#------------------------------permissions----------------------------------

echo "Adding user to docker group..."

sudo usermod -aG docker $USER && newgrp docker

echo "docker is now working"
