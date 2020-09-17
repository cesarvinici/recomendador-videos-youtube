#!/bin/bash

echo "Pushing..."
heroku container:push web -a murmuring-peak-72081

echo "Releasing..."
heroku container:release web -a murmuring-peak-72081
echo "Opening..."
heroku open -a murmuring-peak-72081