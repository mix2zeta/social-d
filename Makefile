format:
	docker-compose down
	docker-compose up -d social-d-db
	docker-compose run --rm social-d-db bash -c '/app/schema/bootstrap.sh'
start:

stop:

tests: