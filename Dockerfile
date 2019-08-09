FROM dyne/devuan:beowulf
ENV debian buster

LABEL maintainer="Puria Nafisi Azizi <puria@dyne.org>" \
	  homepage="https://github.com/decodeproject/petition-tp-python"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update -y -q \
	&& apt-get install -y -q \
    pkg-config \
    python3 \
    python3-pip \
    python3-stdeb \
	python3-dev \
    python3-protobuf \
    python3-cbor \
    python3-colorlog \
    python3-toml \
    python3-yaml \
    python3-zmq \
    && apt-get clean

RUN pip3 install grpcio-tools wheel

RUN mkdir -p /var/log/sawtooth /project

COPY src /project/petition-tp-python
RUN pip3 install -e /project/petition-tp-python

ENV PATH=$PATH:/project/petition-tp-python/bin
WORKDIR /project/petition-tp-python

CMD petition-tp-python
