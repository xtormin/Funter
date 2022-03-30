docker run -p 5434:5432 --name formshunterdb -v $(pwd)/database:/var/lib/postgresql/data -e POSTGRES_PASSWORD=secret -d postgres
docker start formshunterdb