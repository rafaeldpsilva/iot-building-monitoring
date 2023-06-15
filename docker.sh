#!/bin/bash

cp ~/Documentos/gecad/TIoCPS/left-config.json config/config.json
docker rmi rdpds/tiocps-left-monitoring:latest

docker build -t rdpds/tiocps-left-monitoring .
id=$(docker images | grep 'rdpds/tiocps-left-monitoring' | head -1 | awk '{print $3}')
echo "ID: $id"
docker tag $id rdpds/tiocps-left-monitoring:latest
docker push --all-tags rdpds/tiocps-left-monitoring



cp ~/Documentos/gecad/TIoCPS/right-config.json config/config.json
docker rmi rdpds/tiocps-right-monitoring:latest

docker build -t rdpds/tiocps-right-monitoring .
id=$(docker images | grep 'rdpds/tiocps-right-monitoring' | head -1 | awk '{print $3}')
echo "ID: $id"
docker tag $id rdpds/tiocps-right-monitoring:latest
docker push --all-tags rdpds/tiocps-right-monitoring


cp ~/Documentos/gecad/TIoCPS/pedro-config.json config/config.json
docker rmi rdpds/tiocps-h1-monitoring:latest

docker build -t rdpds/tiocps-h1-monitoring .
id=$(docker images | grep 'rdpds/tiocps-h1-monitoring' | head -1 | awk '{print $3}')
echo "ID: $id"
docker tag $id rdpds/tiocps-h1-monitoring:latest
docker push --all-tags rdpds/tiocps-h1-monitoring


cp ~/Documentos/gecad/TIoCPS/luis-config.json config/config.json
docker rmi rdpds/tiocps-h2-monitoring:latest

docker build -t rdpds/tiocps-h2-monitoring .
id=$(docker images | grep 'rdpds/tiocps-h2-monitoring' | head -1 | awk '{print $3}')
echo "ID: $id"
docker tag $id rdpds/tiocps-h2-monitoring:latest
docker push --all-tags rdpds/tiocps-h2-monitoring

