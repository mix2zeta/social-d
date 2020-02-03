format:
	docker-compose down
	docker-compose up -d social-d-db
	docker-compose run --rm social-d-db bash -c '/app/schema/bootstrap.sh'
start:

stop:

tests:
	docker-compose down
	docker-compose up -d social-d-db
	docker-compose run --rm -e PGDBNAME='test_social' social-d-db bash -c '/app/schema/bootstrap.sh'
	docker-compose run --rm -e PGDBNAME='test_social' social-d-service pytest -vv --cov-report term-missing --cov=. --cov-config .coveragerc $*