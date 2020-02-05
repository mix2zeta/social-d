format:
	sudo rm -rf src/split_data/* src/media/*
	docker-compose down
	docker-compose up -d social-d-db social-d-redis
	docker-compose run --rm social-d-db bash -c '/app/schema/bootstrap.sh'
	docker-compose run --rm social-d-service bash -c 'python worker/init_schedule.py'
	docker-compose up -d
start:
	docker-compose up -d
stop:
	docker-compose down
tests:
	sudo rm -rf src/worker/test/test_split_data/* src/tests/test_media/*
	docker-compose down
	docker-compose up -d social-d-db social-d-redis
	docker-compose run --rm -e PGDBNAME='test_social' social-d-db bash -c '/app/schema/bootstrap.sh'
	docker-compose run --rm -e PGDBNAME='test_social' social-d-service pytest -vv --cov-report term-missing --cov=. --cov-config .coveragerc

psql:
	docker exec -it social-d-db psql -U postgres -d social_service