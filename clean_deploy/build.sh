#!/bin/bash

echo "Stoping Container"
docker stop ytrec
echo "Removing container"
docker container rm ytrec
echo "Building Container"
docker build . -t ytrec