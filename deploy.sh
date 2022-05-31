#!/bin/sh

cp .env.sample .env
export DATABASE_URL="postgresql://postgresql:yoursupersecret@localhost:10021/templaterdb?schema=public"
docker-compose -f docker-compose-gitpod.yml up -d --build