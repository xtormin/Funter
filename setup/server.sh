docker run -p 5432:5432 --name formshunterdb -v /Users/j4ckmln/Xtormin/Development/Dev/formshunter/database:/var/lib/postgresql/data -e POSTGRES_PASSWORD=secret -d postgres
docker start formshunterdb