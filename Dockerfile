FROM python:3

WORKDIR /

ADD ./ /
ADD ./convert_pubtator /bin

RUN mkdir -p /data && mkdir -p /work
RUN pip install rdflib

ENTRYPOINT [ "convert_pubtator" ]




