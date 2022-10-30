export APP_IP="127.0.0.1"
export APP_PORT="8080"

#python /home/ivaaahn/dev/retailer/retailer/tests/cache/cache_load.py
docker run --rm --network="host" \
           -v `pwd`/scripts:/scripts \
           -v `pwd`/data:/data \
           czerasz/wrk-json wrk -c8 -t8 -d60s -s /scripts/multi-request-json.lua http://$APP_IP:$APP_PORT