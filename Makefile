.PHONY: up down build sh test lint fmt migrate run

build:   ## build docker image
	docker compose build

up:      ## รันเว็บที่ http://localhost:8000
	docker compose up

down:
	docker compose down

sh:      ## เข้า shell ใน container
	docker compose run --rm web bash

test:    ## รัน pytest ทั้งชุด
	docker compose run --rm --profile tools test

lint:
	docker compose run --rm web ruff check .

fmt:
	docker compose run --rm web ruff format .

migrate:
	docker compose run --rm web python manage.py migrate

run:
	python manage.py runserver
