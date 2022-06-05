#! /bin/bash

echo "[>] Starting downing"

# shellcheck disable=SC2164
cd ~/retailer/deploy/
docker-compose --env-file /home/www/retailer/deploy/.env.docker-compose down

echo "[>] Downing done."
