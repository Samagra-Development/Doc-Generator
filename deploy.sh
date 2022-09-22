#!/bin/sh

cp .env.sample .env
export DATABASE_URL="postgresql://postgresql:yoursupersecret@localhost:10021/templaterdb?schema=public"
docker-compose -f docker-compose-gitpod.yml up -d --build

docker exec doc-generator-web-1 python3 manage.py makemigrations
docker exec doc-generator-web-1 python3 manage.py migrate

echo "wait for 30 sec to let container start"
sleep 30 # let container start
