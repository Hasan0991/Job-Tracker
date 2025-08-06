#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -U "postgres"; do
  echo "Waiting for database at $host..."
  sleep 2
done

echo "Database is ready, starting application..."

exec $cmd
