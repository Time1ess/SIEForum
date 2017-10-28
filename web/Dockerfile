FROM python:3.5
MAINTAINER youchen <youchen.du@gmail.com>
USER root

RUN apt-get update
RUN apt-get install vim gettext -y
RUN apt-get install cron -y

RUN pip install Misago==0.13.0 uwsgi Celery
RUN pip install redis
RUN pip install numpy

ADD SIEForum_uwsgi.ini /SIEForum_uwsgi.ini
ADD entrypoint.sh /entrypoint.sh
RUN chmod a+x entrypoint.sh

EXPOSE 8000
EXPOSE 8001

ENTRYPOINT ["/entrypoint.sh"]
