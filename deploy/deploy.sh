#! /bin/bash

echo $1
echo $2
retailer_tag=$1
retailer_admin_tag=$2

echo "  [>] Starting deployment"

echo "  [+] Remove containers, volume and networks older than 1 week..."
docker system prune --force --filter "until=168h"

# shellcheck disable=SC2164
cd ~/retailer/deploy/

export RETAILER_VERSION=$retailer_tag
export RETAILER_ADMIN_VERSION=$retailer_admin_tag
export PYMAILER_VERSION=0.1
export RABBITMQ_VERSION=0.1

echo "  [+]  Retailer Version: : $retailer_tag"
echo "  [+]  Retailer-Admin Version: $retailer_admin_tag"


echo "  [+] Start (or Restart) containers: docker-compose up -d"
docker-compose --env-file /home/www/retailer/deploy/.env.docker-compose -f /home/www/retailer/deploy/docker-compose.yml up -d

echo "[>] Deployment done."
