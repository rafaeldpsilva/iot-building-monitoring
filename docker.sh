docker build -t rdpds/building-api .
docker tag rdpds/building-api rdpds/building-api:latest
docker tag rdpds/building-api rdpds/building-api:v0.1.32
docker push --all-tags rdpds/building-api