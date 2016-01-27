apt-get update
apt-get -y upgrade
apt-get install -y python3 python3-pip  build-essential libssl-dev \
                        uwsgi-plugin-python3 wget python-software-properties \ 
                        libffi-dev python3-dev software-properties-common \
                        supervisor python3-setuptools python2.7-dev
                        # lighttpd lighttpd-doc \

wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

apt-get install -y postgresql python-psycopg2 libpq-dev

# get code
cd /home/www-user
git clone https://github.com/rim99/bottle-blog.git

# ln -s /home/www-user/bottle-blog/lighttpd.conf /etc/lighttpd/lighttpd.conf

pip3 install cffi bottle tornado psycopg2 jinja2 misaka Pygments houdini.py

cat << EOF > /etc/init.d/create_new_database.sh
createdb -E UTF8 --lc-collate=zh_CN.UTF-8 --lc-ctype=zh_CN.UTF-8 -T template0 BlogDatabase
psql -U www-user -d BlogDatabase -c "CREATE TABLE blogpost ( id serial PRIMARY KEY, title varchar,  category  varchar,  content text, blogID varchar, postdate timestamp, url varchar);"           
sudo rm /etc/init.d/create_new_database.sh
sudo rm /etc/rc.d/rc3.d/c_n_d.sh
EOF
chomd u+x /etc/init.d/create_new_database.sh
ln -s /etc/init.d/create_new_database.sh /etc/rc.d/rc3.d/c_n_d.sh

echo "python3 /home/www-user/bottle-blog/app.py" > /etc/init.d/blog_start.sh
chomd u+x /etc/init.d/blog_start.sh
ln -s /etc/init.d/blog_start.sh /etc/rc.d/rc3.d/blog_start.sh

echo "Please manually run the command \"sudo reboot now\" to continue"


