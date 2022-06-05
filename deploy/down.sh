#! /bin/bash

echo "[>] Starting downing"

# shellcheck disable=SC2164
cd ~/retailer/deploy/

echo "[>] docker-compose down..."
docker-compose --env-file /home/www/retailer/deploy/.env.docker-compose down


echo "[>] docker stop all containers"
# shellcheck disable=SC2046
docker stop $(docker ps -a -q)

echo "[>] docker remove all containers"
# shellcheck disable=SC2046
docker rm $(docker ps -a -q)

echo "[>] docker remove images retailer and retailer-admin"
docker rmi ivaaahn/retailer:latest
docker rmi ivaaahn/retailer-admin:latest


sudo chmod +w pg/scripts

echo "[>] Downing is done."
