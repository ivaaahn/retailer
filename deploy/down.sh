#! /bin/bash

echo "[>>>] Downing..."

cd ~/retailer/ || exit

echo "[>] Docker compose down..."
docker compose down

echo "[>] Docker stop all containers..."
# shellcheck disable=SC2046
docker stop $(docker ps -a -q)

echo "[>] Docker remove all containers..."
# shellcheck disable=SC2046
docker rm $(docker ps -a -q)

echo "[>] Docker remove images retailer and retailer-admin"
docker rmi ivaaahn/retailer:latest
docker rmi ivaaahn/retailer-admin:latest

echo "[>] Downing is done."
