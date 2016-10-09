killall nginx 
sleep 2 
nginx -c $PWD/nginx-bottle.conf &
python3 app.py &
