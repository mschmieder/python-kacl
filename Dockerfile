FROM python:3-slim

COPY . /src

RUN cd src && python /src/setup.py install \
    && rm -rf /src

ENTRYPOINT [ "kacl-cli" ]