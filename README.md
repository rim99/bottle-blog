# About

This is a personal blog app based on [Bottle](http://bottlepy.org/), and uses [Tornado](http://www.tornadoweb.org/en/stable/) as its HTTP server, which all support Python3.x. Visit [my blog](http://www.rim99.com) to see what it's like.

## How to use

### Deployment

Use `deploy.sh` to complete the deployment. 

### Database Deatil

The project uses [PostgreSQL](www.postgresql.org) as its database. The following table shows the structure of the data table:
 
item     | type
:-:      | :-:
title    | varchar NOT NULL
tag1     | varchar NOT NULL
tag2     | varchar
tag3     | varchar
content  | text NOT NULL
blogID   | varchar NOT NULL PRIMARY KEY
postdate | timestamp
url      | varchar NOT NULL

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
