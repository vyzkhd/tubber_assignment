# tubber_assignment
Business rules framework on eventstreams using FastAPI

1) After pulling the files, run  docker-compose build from the terminal. This will build 3 containers 
     a) PostgreSQL database at 5432
     b) web container at 8000
     c) pgadmin at 5050 (creds in docker-compose.yml)

2) Make migrations 
          docker-compose run web alembic revision --autogenerate -m "first  migration"
3) run docker-compose up
