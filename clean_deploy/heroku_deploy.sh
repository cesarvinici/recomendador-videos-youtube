#!/bin/bash

echo "Pushing..."
heroku container:push web -a cesar-youtube-recomender

echo "Releasing..."
heroku container:release web -a cesar-youtube-recomender
echo "Opening..."
heroku open -a cesar-youtube-recomender