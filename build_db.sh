#!/bin/bash
echo "[INFO] Killing old database process"
docker kill sustain_proj
echo "[INFO] Removing old database image"
docker rm sustain_proj
echo "[INFO] Pulling latest MySQL version"
docker pull mysql/mysql-server:latest
echo "[INFO] Running docker image"
docker run --name sustain_proj -p 3306:3306 -e MYSQL_ROOT_HOST=% -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=root -d mysql/mysql-server