#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

import psycopg2
from asyncio import sleep, get_event_loop
from select import select
from psycopg2.pool import SimpleConnectionPool

DATABASE_NAME = 'BlogDatabase'
HOST = 'localhost'
USER_NAME = 'rim99'
PASSWORD = 'passwd'
# USER_NAME = 'root'
# PASSWORD = 'passwd'

class Task(object):
    '''Task obj contains these info:
    1. the sql cmd about to execute
    2. a connection obj of a pipe to pass the result
    3. the result type: obj or list; because different functions need to be executed based on that
       the result_type can be two options: "obj" or "list", corresponding to a single query obj or a set of objs"'''
    def __init__(self, sql_cmd, send_conn, result_type):
        self.sql_cmd = sql_cmd
        self.send_conn = send_conn
        self.result_type = result_type

class AsyncConnectionPool(SimpleConnectionPool):
    '''Rewrite a async blocking version
        The object contains the following params:
            1. self._pool  # contains available conn
            2. self._used  # conatins the using conn
            3. self._rused  # id(conn) -> key map
            4. self._keys
    '''
    async def getconn(self, key=None):
        """Get a free connection and assign it to 'key' if not None."""
        if self.closed:
            raise Exception("Connection pool is closed")
        if key is None:
            key = self._getkey()
        if key in self._used:
            return self._used[key]
        while True:
            if self._pool:
                # add the new conn into the Dict: _used;
                # new conn is popped from the available list:_pool
                self._used[key] = conn = self._pool.pop()
                self._rused[id(conn)] = key
                return conn
            await sleep(0.1) # LOW EFFICIENCY

async def ready(conn):
    while True:
        state = conn.poll()
        if state == psycopg2.extensions.POLL_OK:
            break
        elif state == psycopg2.extensions.POLL_WRITE:
            select([], [conn.fileno()], [])
        elif state == psycopg2.extensions.POLL_READ:
            select([conn.fileno()], [], [])
        else:
            raise psycopg2.OperationalError("poll() returned %s" % state)

async def process_task(pool, task):
    conn = await pool.getconn()
    await ready(conn)
    acurs = conn.cursor()
    jobs_dict = {'obj': acurs.fetchone,
                 'list': acurs.fetchall}
    acurs.execute(task.sql_cmd)
    await ready(acurs.connection)
    result = jobs_dict[task.result_type]()
    task.send_conn.send(result)
    pool.putconn(conn)

def db_query_service(task_queue, thread_num):
    pool = AsyncConnectionPool(minconn=1, maxconn=4, database=DATABASE_NAME, user=USER_NAME, async=True)
    loop = get_event_loop()
    while True:
        try:
            task = task_queue.get()
            loop.run_until_complete(process_task(pool, task))
        except Exception as msg:
            print(msg)

def db_update(sql_cmd):
    dbconn = psycopg2.connect(database=DATABASE_NAME, user=USER_NAME)
    cursor = dbconn.cursor()
    cursor.execute(sql_cmd)
    dbconn.commit()
    cursor.close()
    dbconn.close()
