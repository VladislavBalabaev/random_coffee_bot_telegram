# to ensure bot has db connection when stopping:
docker stop nespresso_bot
docker stop nespresso_api
docker stop nespresso_db
# docker compose stop
docker compose down

docker compose build #--no-cache
docker compose up --detach
# docker exec -it nespresso_bot bash

docker compose logs -f bot
