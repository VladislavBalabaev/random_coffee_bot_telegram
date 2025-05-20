docker compose stop
docker compose down

docker compose build #--no-cache
docker compose up --detach
# docker exec -it nespresso_bot bash

docker compose logs -f bot
