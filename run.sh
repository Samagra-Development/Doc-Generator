#!/bin/bash

if [[ $1 = "start" ]]
then
	echo "starting services"
    yarn install
    docker-compose up -d
    yarn start:dev
elif [[ $1 = "stop" ]]
then
	echo "not ok"
    docker-compose down
elif [[ $1 = "--help" ]]
then
    echo "Usage: run.sh [COMMAND]"
    echo "Commands:"
    echo "start    start all services"
    echo "stop     stop all services"
else
    echo "Invalid Command"
fi