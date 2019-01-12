DK=docker
DC=docker-compose
BASE=docker-compose.yml
LOCAL=docker-compose.local.yml
PROD=docker-compose.prod.yml
BASE_AND_LOC=-f $(BASE) -f $(LOCAL)
BASE_AND_PROD=-f $(BASE) -f $(PROD)
DB_IMG=mdillon/postgis:9.6

.PHONY: logs dev

# Gets docker-compose.yml images and local builds
build:
	@$(DC) pull
	@$(DC) build

# Runs services
up:
	@$(DC) $(BASE_AND_LOC) up

# Runs services in detached mode
upd:
	@$(DC) $(BASE_AND_LOC) up -d

# Stops services
down:
	@$(DC) down

# Restarts services
restart:
	@$(DC) restart

# List running services:
ps:
	@$(DC) ps

# Print all logs
logs:
	@$(DC) logs

# Watch all logs
watchl:
	@$(DC) logs -f

# Show Nginx container logs
logn:
	@$(DC) logs nginx

# Show web container logs
logw:
	@$(DC) logs web

# Watch Nginx container logs
watchn:
	@$(DC) logs -f nginx

# Watch web container logs
watchw:
	@$(DC) logs -f web

# Reload uwsgi server
reload:
	@touch reload.ini

# Bash inside web container
bashw:
	@$(DC) exec web bash

# Bash inside Nginx container
bashn:
	@$(DC) exec nginx bash

# Bash inside db container
bashd:
	@$(DC) exec db bash

# Generate self signed SSL key
ssl:
	@./ssl.sh

# Run production docker compose
prod:
	@$(DC) $(BASE_AND_PROD) up -d

# Migrate local
migratelocal:
	@$(DC) $(BASE_AND_LOC) exec web python manage.py makemigrations
	@$(DC) $(BASE_AND_LOC) exec web python manage.py migrate

# Compiles requirements*.in
compile:
	@pip-compile
	@pip-compile --output-file requirements-dev.txt requirements-dev.in

# Installs requirements
reqs:
	@pip install -r requirements.txt -r requirements-dev.txt

# Stop all containers and removes them
stop:
	@$(DK) stop $(shell $(DK) ps -a -q) \
		&& $(DK) rm $(shell $(DK) ps -a -q)

# Starts Django development server
start:
	@DB_IMG=$(DB_IMG) ./start.sh
