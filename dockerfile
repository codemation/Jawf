FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3-pip \ 
                    curl \
                    git


CMD ["echo", "test"]


FROM joshjamison/ubuntu-python:latest
RUN git clone https://github.com/codemation/pyql

CMD ["sleep 100"]