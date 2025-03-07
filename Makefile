dev:
	docker compose -f docker-compose.dev.yaml up --build

prod:
	docker compose up --build

genclient:
	sudo rm -rf OnixDjClient && \
	(cd backend && python3 manage.py spectacular --file api-schema.yml) && \
    docker run --rm -v $(PWD):/local openapitools/openapi-generator-cli generate \
        -i /local/backend/api-schema.yml \
        -g typescript-fetch \
        -o /local/OnixDjClient \
        --additional-properties=npmName=onix-api,npmVersion=1.0.0 && \
	rm backend/api-schema.yml && \
	sudo chmod 777 -R OnixDjClient && \
	(cd OnixDjClient && npm i)