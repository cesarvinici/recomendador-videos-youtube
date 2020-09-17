#!/bin/bash


echo "Removing old images"
docker ps -a | awk '{ print $1,$2 }' | grep ytrec | awk '{print $1 }' | xargs -I {} docker rm {}
echo "Building Container"
docker build . -t ytrec
echo "Running container"
docker run --name=ytrec -e PORT=80 -p 80:80 ytrec