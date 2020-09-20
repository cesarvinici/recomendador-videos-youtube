#!/bin/bash
docker rm -f ytrec
echo "Running container"
docker run  --name=ytrec \
    -v ~/Documents/DS/recomendador-videos-youtube/clean_deploy/src:/app/ \
    -e PORT=80 -p 80:80 \
    -d ytrec