apt-get update
apt-get -y upgrade
apt-get install -y python3 python3-pip uwsgi \
                        uwsgi-plugin-python3 wget python-software-properties \ 
                        build-essential libssl-dev lighttpd lighttpd-doc \
                        libffi-dev python3-dev software-properties-common \
                        supervisor python3-setuptools python2.7-dev

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

apt-get install -y postgresql python-psycopg2 libpq-dev

# add new user 
useradd 'www-user' 
echo 'www-passwd'|passwd

# configure database setting 

createdb BlogDatabase
psql -U www-user -d BlogDatabase -c       \ 
"CREATE TABLE blogpost (      \
id       serial PRIMARY KEY,  \
title     varchar,            \
category  varchar,            \
content   text,               \
blogID    varchar,            \
postdate  timestamp,          \
url       varchar);"           

cd /home/www-user
git clone https://github.com/rim99/bottle-blog.git

ln -s /home/www-user/bottle-blog/lighttpd.conf /etc/lighttpd/lighttpd.conf

pip3 install bottle tornado psycopg2 jinja2 misaka Pygments houdini.py

