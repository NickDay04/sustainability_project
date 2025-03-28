#!/bin/bash
echo "[INFO] Killing old database process"
docker kill alder_db
echo "[INFO] Removing old database image"
docker rm alder_db
echo "[INFO] Pulling latest MySQL version"
docker pull mysql/mysql-server:latest
echo "[INFO] Running docker image"
docker run --name alder_db -p 3306:3306 -e MYSQL_ROOT_HOST=% -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=root -d mysql/mysql-server