#!/bin/sh
set -e

host="${DB_HOST:-localhost}"
user="${DB_USER:-postgres}"
shift
cmd="$@"

until pg_isready -h "$host" -U "$user"; do
  echo "Waiting for database at $host..."
  sleep 2
done

echo "Database is ready, starting application..."

exec $cmd
