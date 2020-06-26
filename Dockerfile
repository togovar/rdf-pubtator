FROM python

WORKDIR /

ADD ./ /
ADD ./convert_pubtator /bin

RUN mkdir /data
RUN pip install rdflib

ENTRYPOINT [ "convert_pubtator" ]




