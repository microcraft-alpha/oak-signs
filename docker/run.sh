#!/bin/bash

set -exo pipefail

echo "Waiting for Mongo..."

while ! nc -z mongodb 27017; do
	sleep 0.1
done

echo "MongoDB started"

if [[ -z ${DEVELOPMENT} ]]; then

	COMMAND=("$(which uvicorn)" "oak_signs.main:app" "--limit-max-requests=10000" "--timeout-keep-alive=2" "--workers" "1" "--host" "0.0.0.0" "--port" "${PORT:-8004}")

else

	COMMAND=("$(which uvicorn)" "oak_signs.main:app" "--reload" "--workers" "1" "--host" "0.0.0.0" "--port" "${PORT:-8004}")

fi

exec "${COMMAND[@]}"
