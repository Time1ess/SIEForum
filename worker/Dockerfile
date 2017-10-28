FROM python:3.5
MAINTAINER youchen <youchen.du@gmail.com>
USER root

ADD entrypoint.sh /entrypoint.sh

RUN pip install Misago==0.13.0 uwsgi Celery numpy redis

RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
