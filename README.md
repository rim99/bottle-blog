This is my blog app based on [Bottle](http://bottlepy.org/)

## Initalization

### Manually Create the Database and the data table.
'''createdb BlogDatabase'''
"""CREATE TABLE blogpost (
            id serial PRIMARY KEY,
            title varchar,
            category varchar,
            content text,
            blogID varchar,
            postdate varchar,
            url varchar);"""
