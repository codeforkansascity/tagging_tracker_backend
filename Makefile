DC=docker-compose

# Gets docker-compose.yml images and local builds
build:
	@$(DC) pull
	@$(DC) build

# Runs services
up:
	@$(DC) up

# Runs services in detached mode
upd:
	@$(DC) up -d

# Stops services
down:
	@$(DC) down

# Restarts services
restart:
	@$(DC) restart

# List running services:
ps:
	@$(DC) ps

# Show Nginx container logs
nlogs:
	@$(DC) logs nginx

# Show uwsgi container logs
ulogs:
	@$(DC) logs uwsgi

# Watch Nginx container logs
watchn:
	@$(DC) logs -f nginx

# Watch uwsgi container logs
watchu:
	@$(DC) logs -f uwsgi
