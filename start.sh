#!/usr/bin/env bash

checkenv() {
    if [[ -z "$1" ]]; then
        echo "$2 not set in local.env"
        exit 1
    fi
}

if [ ! -f local.env ]; then
    echo "local.env not found"
    exit 1
fi

source local.env

checkenv "$DB_NAME" "DB_NAME"
checkenv "$DB_USER" "DB_USER"
checkenv "$DB_PASSWORD" "DB_PASSWORD"

export DEBUG=1

# Check to see if we are already running the image
if docker ps | grep $DB_IMG -q; then

    # Check if we have unapplied migrations
    if python -W ignore manage.py showmigrations --plan | grep "\[ \]" -q; then
        echo "Migrations found"
        python -W ignore manage.py makemigrations
        python -W ignore manage.py migrate
        make start
    else
        echo "No pending migrations"

        # Check that DB container is up and running
        if ! [ -x "$(command -v nc)" ]; then
            echo "netcat not on system."
            echo "If django server fails to connect to db press Ctrl+C and run 'make start' again"
        else
            while ! nc -z localhost 5432; do
                echo "Waiting for DB container to boot"
                sleep 0.2 # wait for 2/10 of the second before check again
            done
        fi

        # Run dev server
        python manage.py runserver
    fi
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
    make start
fi
