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

# RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
RUN perl -p -i.orig -e 's/archive.ubuntu.com/mirrors.aliyun.com\/ubuntu/' /etc/apt/sources.list
RUN apt-get update
# RUN apt-get install -y build-essential git
# RUN apt-get install -y python python-dev python-setuptools
# RUN apt-get install -y nginx 
# RUN easy_install pip
RUN apt-get -y upgrade
RUN apt-get install -y python3 python3-pip uwsgi \
                        uwsgi-plugin-python \
                        build-essential libssl-dev \
                        libffi-dev python3-dev \
                        supervisor python3-setuptools
RUN easy_install pip 

# install uwsgi now because it takes a little while
RUN pip install uwsgi

# install nginx
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update -y
RUN apt-get install -y python-software-properties nginx # add 'nginx'

# install PostgreSQL
# RUN apt-get install -y sqlite3
RUN apt-get install -y postgresql python-psycopg2 libpq-dev

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

# install django, normally you would remove this step because your project would already
# be installed in the bottle-blog/app/ directory
# RUN django-admin.py startproject website /home/docker/bottle-blog/app/ 

expose 80
# cmd ["supervisord", "-n"]
