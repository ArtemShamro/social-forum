#!/bin/sh

set -e

hosts="$@"

for host in $hosts; do
  until nc -z $(echo $host | tr ':' ' '); do
    echo "Waiting for $host..."
    sleep 2
  done
done

exec "${@: -2}"
