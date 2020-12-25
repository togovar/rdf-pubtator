FROM python

WORKDIR /

ADD ./ /
ADD ./convert_pubtator /bin

RUN mkdir /data && mkdir /work
RUN pip install rdflib

ENTRYPOINT [ "convert_pubtator" ]




