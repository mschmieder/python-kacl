#/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

version=$(cat VERSION)

docker build -t mschmieder/kacl-cli:${version} .
docker push mschmieder/kacl-cli:${version}
docker tag mschmieder/kacl-cli:${version} mschmieder/kacl-cli:latest
docker push mschmieder/kacl-cli:latest

# add changelog to docker hub
docker run -v $PWD:/workspace \
    -e DOCKERHUB_USERNAME=$DOCKER_USERNAME \
    -e DOCKERHUB_PASSWORD=$DOCKER_PASSWORD \
    -e DOCKERHUB_REPOSITORY="mschmieder/kacl-cli" \
    -e README_FILEPATH='/workspace/README.md' \
    peterevans/dockerhub-description:2.1.0