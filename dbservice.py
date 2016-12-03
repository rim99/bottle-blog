#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Rim99'

import psycopg2, concurrent.futures, threading

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


def db_query_service(task_queue, thread_num):
    dbconn = psycopg2.connect(database=DATABASE_NAME, user=USER_NAME)
    lock = threading.Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num):
        cursor = dbconn.cursor()
        jobs_dict = {'obj': cursor.fetchone,
                     'list': cursor.fetchall}
        try:
            while True:
                lock.acquire()
                task = task_queue.get()
                lock.release()
                cursor.execute(task.sql_cmd)
                result = jobs_dict[task.result_type]()
                task.send_conn.send(result)
        except Exception as msg:
            print(msg)
            cursor.close()
    dbconn.close()

def db_update(sql_cmd):
    dbconn = psycopg2.connect(database=DATABASE_NAME, user=USER_NAME)
    cursor = dbconn.cursor()
    cursor.execute(sql_cmd)
    dbconn.commit()
    cursor.close()
    dbconn.close()
