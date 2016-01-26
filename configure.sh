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

mkdir /home/www/
cd /home/www
git clone https://github.com/rim99/bottle-blog.git

ln -s /home/docker/bottle-blog/lighttpd.conf /etc/lighttpd/lighttpd.conf

pip3 install bottle tornado psycopg2 jinja2 misaka Pygments houdini.py

