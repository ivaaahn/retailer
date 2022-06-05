#! /bin/bash

echo "  [>] Starting deployment"

echo "  [+] Remove containers, volume and networks older than 1 week..."
docker system prune --force --filter "until=1h"

# shellcheck disable=SC2164
cd ~/retailer/deploy/

export RETAILER_VERSION=$1
export RETAILER_ADMIN_VERSION=$2
export PYMAILER_VERSION=0.1
export RABBITMQ_VERSION=0.1

echo "  [+]  Retailer Version: : $RETAILER_VERSION"
echo "  [+]  Retailer-Admin Version: $RETAILER_ADMIN_VERSION"
echo "  [+]  Pymailer Version: $PYMAILER_VERSION"
echo "  [+]  RabbitMQ Version: $RABBITMQ_VERSION"


echo "  [+] Start (or Restart) containers: docker-compose up -d"
docker-compose --env-file /home/www/retailer/deploy/.env.docker-compose -f /home/www/retailer/deploy/docker-compose.yml up -d

echo "[>] Deployment done."
