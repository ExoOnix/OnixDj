dev:
	docker compose -f docker-compose.dev.yaml up --build

prod:
	docker compose up --build

genschema:
	(cd backend && python3 manage.py spectacular --file ../frontend/api-schema.yml)