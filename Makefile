.PHONY: dev build up migrate shell dbshell redis-cli test

COMPOSE-DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
COMPOSE-TEST = docker-compose -f docker-compose.yml -f docker-compose.test.yml
FILE = $(file)

dev:
	if [ ! -f .env ]; then touch .env; fi;
	$(COMPOSE-DEV) up --build

build:
	$(COMPOSE-DEV) build

up:
	$(COMPOSE-DEV) up

stop:
	$(COMPOSE-DEV) down

migrate:
	$(COMPOSE-DEV) exec indoor flask db migrate

upgrade:
	$(COMPOSE-DEV) exec indoor flask db upgrade

shell:
	$(COMPOSE-DEV) exec indoor flask debug

bash:
	$(COMPOSE-DEV) exec indoor /bin/sh

dbshell:
	$(COMPOSE-DEV) exec indoor flask dbshell

redis-cli:
	$(COMPOSE-DEV) exec indoor-redis redis-cli

test:
	if [ ! -f .env ]; then touch .env; fi;
	TEST_FILE=$(FILE) $(COMPOSE-TEST) up --build --scale indoor-redis=0 --abort-on-container-exit

db:
	$(COMPOSE-DEV) exec indoor flask db init
