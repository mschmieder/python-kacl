FROM python:3-slim

RUN apt update && apt-get install -y git

COPY . /src

RUN cd src && python /src/setup.py install \
    && rm -rf /src

ENTRYPOINT [ "kacl-cli" ]