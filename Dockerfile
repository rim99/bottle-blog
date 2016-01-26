#  BY rim99 aka ZHANG, Xin

FROM ubuntu:14.04

MAINTAINER Dockerfiles

RUN apt-get update --fix-missing 
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip  build-essential libssl-dev \
                        uwsgi-plugin-python3 wget python-software-properties \ 
                        libffi-dev python3-dev software-properties-common \
                        supervisor python3-setuptools python2.7-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# install PostgreSQL
RUN apt-get install -y postgresql python-psycopg2 libpq-dev


# add new user 
RUN useradd 'www-user' 
RUN echo 'www-passwd'|passwd
RUN echo 'www-passwd'|passwd
RUN echo '123' # full name
RUN echo '123' # room no. 
RUN echo '123' # work phone.
RUN echo '123' # home phone.
RUN echo '123' # other
RUN echo 'y' # Confirmation

# configure database setting 

RUN createdb BlogDatabase
RUN psql -U www-user -d BlogDatabase -c       \ 
"CREATE TABLE blogpost (      \
id       serial PRIMARY KEY,  \
title     varchar,            \
category  varchar,            \
content   text,               \
blogID    varchar,            \
postdate  timestamp,          \
url       varchar);"           

# install our code
ADD . /home/www-user/bottle-blog/

RUN pip3 install bottle tornado psycopg2 jinja2 misaka Pygments houdini.py

expose 80
# cmd ["supervisord", "-n"]

RUN python3 /home/www-user/bottle-blog/app.py 
