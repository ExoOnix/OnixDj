dev:
	docker compose -f docker-compose.dev.yaml up --build

prod:
	docker compose up --build

genclient:
	(cd backend && python3 manage.py spectacular --file api-schema.yml) && \
    docker run --rm -v $(PWD):/local openapitools/openapi-generator-cli generate \
        -i /local/backend/api-schema.yml \
        -g typescript-fetch \
        -o /local/OnixDjClient && \
	rm backend/api-schema.yml