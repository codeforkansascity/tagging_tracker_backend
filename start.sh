#!/usr/bin/env bash

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
        python manage.py runserver
    fi
else
    echo "DB container not found"
    echo "starting..."
    docker run \
        --rm \
        -d \
        -p 5432:5432 \
        -v db-data:/var/lib/postgresql/data \
		-e POSTGRES_PASSWORD=pass \
		-e POSTGRES_USER=dev_user \
		-e POSTGRES_DB=dev \
		$DB_IMG
    echo "started!"
    make start
fi
