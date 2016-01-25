# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ===========================================================================
# 
# CHANGED FOR DEPLOYING MY BLOG BY rim99 aka ZHANG, Xin
#

FROM ubuntu:14.04

MAINTAINER Dockerfiles

RUN apt-get update --fix-missing 
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip uwsgi \
                        uwsgi-plugin-python3 wget \
                        build-essential libssl-dev \
                        libffi-dev python3-dev software-properties-common \
                        supervisor python3-setuptools python2.7-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

# install nginx
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update -y
RUN apt-get install -y python-software-properties nginx # add 'nginx'

# install PostgreSQL
RUN apt-get install -y postgresql python-psycopg2 libpq-dev

# install uwsgi now because it takes a little while
RUN pip install uwsgi

# install our code
add . /home/docker/bottle-blog/

# setup all the configfiles
# Edit /etc/nginx/sites-enabled/default
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /home/docker/bottle-blog/nginx.conf /etc/nginx/sites-enabled/default  # new

# Edit /etc/uwsgi/apps-available/uwsgi.ini
RUN cat /home/docker/bottle-blog/uwsgi.ini > /etc/uwsgi/apps-available/uwsgi.ini  # new
RUN ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini  # new
# RUN ln -s /home/docker/bottle-blog/supervisor-app.conf /etc/supervisor/conf.d/

# RUN pip install
# RUN pip install -r /home/docker/bottle-blog/app/requirements.txt
RUN pip3 install bottle psycopg2 jinja2 misaka Pygments houdini.py

expose 80
# cmd ["supervisord", "-n"]
