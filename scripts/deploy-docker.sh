#/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

version=$(cat VERSION)

docker build -t mschmieder/kacl-cli:${version} .
docker push mschmieder/kacl-cli:${version}
docker tag mschmieder/kacl-cli:${version} mschmieder/kacl-cli:latest
docker push mschmieder/kacl-cli:latest