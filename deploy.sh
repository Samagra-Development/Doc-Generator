#!/bin/sh

cp .env.sample .env
docker-compose -f docker-compose-gitpod.yml up -d --build