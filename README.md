# THIS README HASN'T FINISHED YET.
# About

This is a personal blog app based on [Bottle](http://bottlepy.org/). Visit [my blog]() to see what it's like.

## How to use





### Database Setting

The project uses [PostgreSQL]() as its database. So, install it first. Then you have to manually create a database and a data table. The structure of the data table is this:
 
item     | type
:-:      | :-:
id       |serial PRIMARY KEY
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
