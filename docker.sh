docker build -t rdpds/building-api .
docker tag rdpds/building-api rdpds/building-api:latest
docker tag rdpds/building-api rdpds/building-api:v0.2.2
docker push --all-tags rdpds/building-api