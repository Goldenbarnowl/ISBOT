#!/bin/bash
cd ..
docker-compose build bot redis
echo "Starting bot and Redis containers..."
docker-compose up -d bot redis
echo "Containers are up and running."
