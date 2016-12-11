#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

import psycopg2, asyncio, datetime
import psycopg2.extensions as _ext
from psycopg2._psycopg import connection as _connection
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

class AsyncConnection(_connection):
    """The connection instance has a special designed attribution -> ref_count.
        The ref_count will plus 1 once the connection instance is using by a coroutine,
        and minus 1 when put by a coroutine.
    """
    def __init__(self, *args, **kwargs):
        super(AsyncConnection, self).__init__(*args, **kwargs)
        self.__dict__['ref_count'] = 0

class AsyncConnectionPool(SimpleConnectionPool):
    """Rewrite an async version.
        The instance contains the following params:
            1. self._pool  # contains available conn
            2. self._used  # conatins the using conn
            3. self._rused  # id(conn) -> key map
            4. self._keys
    """
    def _connect(self, key=None):
        """Create a new connection and assign it to 'key' if not None."""
        conn = psycopg2.connect(*self._args, **self._kwargs,
                                connection_factory=AsyncConnection)
        if key is not None:
            self._used[key] = conn
            self._rused[id(conn)] = key
        else:
            self._pool.append(conn)
        return conn

    def putconn(self, conn, key=None, close=False):
        """Put away a connection."""
        if self.closed:
            raise Exception("connection pool is closed")
        if key is None:
            key = self._rused.get(id(conn))
        if not key:
            raise Exception("trying to put unkeyed connection")
        conn.ref_count -= 1
        if conn.ref_count < 0:
            if len(self._pool) < self.minconn and not close:
                # Return the connection into a consistent state before putting
                # it back into the pool
                if not conn.closed:
                    status = conn.get_transaction_status()
                    if status == _ext.TRANSACTION_STATUS_UNKNOWN:
                        # server connection lost
                        self._pool.remove(conn)
                        conn.close()
                    elif status != _ext.TRANSACTION_STATUS_IDLE:
                        # connection in error or in transaction
                        conn.rollback()
            else:
                self._pool.remove(conn)
                conn.close()
            # here we check for the presence of key because it can happen that a
            # thread tries to put back a connection after a call to close
            if not self.closed or key in self._used:
                del self._used[key]
                del self._rused[id(conn)]

    def getconn(self, key=None):
        """Get a free connection and assign it to 'key' if not None."""
        if self.closed:
            raise Exception("Connection pool is closed")
        if key is None:
            key = self._getkey()
        if key in self._used:
            return self._used[key]
        # return the connection with minimum ref_count
        result = self._pool[0]
        for conn in self._pool[1:]:
            if conn.ref_count < result.ref_count:
                result = conn
        if result.ref_count > 1 and len(self._pool) < maxconn:
            result = self._connect(key)
        # add the new conn into the Dict: _used;
        self._used[key] = result
        self._rused[id(result)] = key
        result.ref_count += 1
        return result

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

async def process_task(pool, task_queue, lock):
    while True:
        conn = pool.getconn()
        acurs = conn.cursor()
        jobs_dict = {'obj': acurs.fetchone,
                     'list': acurs.fetchall}
        try:
            with (await lock):
                task = task_queue.get()
            await ready(conn)
            acurs.execute(task.sql_cmd)
            await ready(conn)
            result = jobs_dict[task.result_type]()
            task.send_conn.send(result)
        except Exception as msg:
            print('Database query service has raised an exception:\n  -->  {0}\n \
                  at time --> {1}\n \
                  when execute CMD: {2}'.format(msg,
                                                datetime.datetime.now()
                                                task.sql_cmd))
        finally:
            acurs.close()
            pool.putconn(conn)

def db_query_service(task_queue, connection_num):
    pool = AsyncConnectionPool(minconn=1, maxconn=connection_num, database=DATABASE_NAME, user=USER_NAME, async=True)
    loop = asyncio.get_event_loop()
    lock = asyncio.Lock()
    tasks = [asyncio.ensure_future(process_task(pool, task_queue, lock))
             for i in range(connection_num*20)]
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except Exception as msg:
        print(msg)
        loop.close()

def db_update(sql_cmd):
    dbconn = psycopg2.connect(database=DATABASE_NAME, user=USER_NAME)
    cursor = dbconn.cursor()
    cursor.execute(sql_cmd)
    dbconn.commit()
    cursor.close()
    dbconn.close()
