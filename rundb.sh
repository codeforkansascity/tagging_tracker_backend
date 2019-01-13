#!/usr/bin/env bash

# This script ensures db container is running

checkenv() {
    if [[ -z "$1" ]]; then
        echo "$2"
        exit 1
    fi
}

source env.sh

checkenv "$DB_IMG" "DB_IMG not set on script invocation"
checkenv "$DB_NAME" "DB_NAME not set in local.env"
checkenv "$DB_USER" "DB_USER  not set in local.env"
checkenv "$DB_PASSWORD" "DB_PASSWORD  not set in local.env"

# Check to see if we are already running the image
if docker ps | grep $DB_IMG -q; then
    echo "DB image already running"
else
    echo "DB container not found"
    echo "starting..."
    docker run \
        -d \
        -p 5432:5432 \
        -v tagging_tracker_backend_db-data:/var/lib/postgresql/data \
		-e POSTGRES_PASSWORD=$DB_PASSWORD \
		-e POSTGRES_USER=$DB_USER \
		-e POSTGRES_DB=$DB_NAME \
		$DB_IMG
    echo "started!"
fi