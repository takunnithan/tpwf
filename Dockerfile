FROM python:3.11.3

RUN mkdir /var/tpwf

COPY server.py /var/tpwf

WORKDIR /var/tpwf

EXPOSE 8000

CMD python server.py
