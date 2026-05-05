migrate:
	docker compose exec user-service alembic upgrade head
	docker compose exec product-service alembic upgrade head
	docker compose exec order-service alembic upgrade head
	docker compose exec payment-service alembic upgrade head

seed:
	cat seed_dev_data.sql | docker compose exec -T postgres psql -U admin -d microservices_db

reset:
	docker compose down -v

logs:
	docker compose logs -f

test:
	pytest

rebuild:
	docker compose up --build -d


bootstrap: 
	docker compose up -d
	sleep 10
	make migrate
	make seed