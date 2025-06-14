@echo off
cd ..
echo Stopping bot and Redis containers...
docker-compose down
echo Containers stopped.
pause
