#! /bin/bash
echo "  [>] Starting deployment"

echo "  [+] Remove containers, volume and networks older than 1h ..."
docker system prune --force --filter "until=1h"

cd ~/retailer/deploy/ || exit

export RETAILER_VERSION=latest
export RETAILER_ADMIN_VERSION=latest
export PYMAILER_VERSION=0.1
export RABBITMQ_VERSION=0.1
export S3_STORAGE_URL=storage.yandexcloud.net
export S3_BUCKET_NAME=retailer-store
export S3_SECRET_USER_AGENT_HEADER=miss
export SU_EMAIL=admin@admin.com
export SU_PSWD=admin


echo "  [+]  Retailer Version: : $RETAILER_VERSION"
echo "  [+]  Retailer-Admin Version: $RETAILER_ADMIN_VERSION"
echo "  [+]  Pymailer Version: $PYMAILER_VERSION"
echo "  [+]  RabbitMQ Version: $RABBITMQ_VERSION"

echo "  [+] Start (or Restart) containers: docker compose up -d"
UID_GID="$(id -u):$(id -g)" docker compose -f /home/www/retailer/docker-compose.yml up -d
echo "Exit status: $?"

echo "[>] Deployment done."
