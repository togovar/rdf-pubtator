FROM python

WORKDIR /

ADD ./ /
ENV PATH $PATH:/

RUN mkdir /data
RUN pip install rdflib

CMD convert_pubtator



