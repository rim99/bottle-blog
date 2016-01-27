# About

This is a personal blog app based on [Bottle](http://bottlepy.org/), and uses [Tornado](http://www.tornadoweb.org/en/stable/) as its HTTP server, which all supports Python3.x. Visit [my blog]() to see what it's like.

## How to use

### Deployment

The `_config/Dockerfile` and `_config/lighttpd.conf` are unavailable right now. 

Use `_config/configure.sh` to complete the deployment. 

### Database Deatil

The project uses [PostgreSQL](www.postgresql.org) as its database. The following table shows the structure of the data table:
 
item     | type
:-:      | :-:
id       | serial PRIMARY KEY
title    | varchar
category | varchar
content  | text
blogID   | varchar
postdate | timestamp
url      | varchar

And you can change it as your wish surely.

### Management

The project uses command-line tool `root/manage.py` to post new articles, overwrite the existed posts, and delete the unwanted posts. The usage is as following.

1. List all blog posts 

    ```python
    python3 manage.py ls
    ```

2. Post new blog 

    ```python3
    python3 manage.py post [file path] [category]
    ```

3. Delete blog

    ```
    python3 manage.py del [blog id]
    ```
    if no blog id provided, the last post will be deleted.

## License

The project is under **MIT LICENSE**.
