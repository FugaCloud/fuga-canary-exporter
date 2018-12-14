FROM python:3.6

ADD ping_exporter /var/lib/ping_exporter
WORKDIR /var/lib/ping_exporter
ADD requirements.txt .
ADD configuration.yaml .
RUN pip install -r requirements.txt
WORKDIR /var/lib