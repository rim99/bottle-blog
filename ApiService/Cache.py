#! /bin/env/python3

import datetime
from tornado.gen import coroutine

time_now = datetime.datetime.now

_cacheAll = dict()

@coroutine
def cacheAsync(cache_name, cache_key, time_alived, func, *kw, **kwargs):
    if time_alived is None:
        # default cache live time is 5 seconds
        time_alived = 5

    concrete_cache = None
    if cache_name in _cacheAll.keys():
        concrete_cache = _cacheAll.get(cache_name)
    else:
        concrete_cache = Cache(cache_name)

    ans = None
    if concrete_cache.hasKey(cache_key):
        ans = concrete_cache.retrive(cache_key)
    if ans is not None:
        return ans
    ans = yield func(*kw, **kwargs)
    concrete_cache.store(cache_key, ans, time_alived)
    return ans


class Cache:
    def __init__(self, name):
        self.cache = dict()
        _cacheAll[name] = self

    def __str__(self):
        return self.cache

    def hasKey(self, key):
        return key in self.cache.keys()

    def retrive(self, key):
        ans = None
        if self.hasKey(key):
            ans = self.cache[key].get()
            if ans is None:
                del self.cache[key]
        return ans

    def store(self, key, value, time_alive):
        item = TimedItem(value, time_alive)
        self.cache[key] = item


class TimedItem:

    def __init__(self, obj, time_alived):
        '''
        :param obj: Any object. Data to save
        :param timeout: int. Time unit: second. If the deadline reached, this item will be droped
        '''
        self.value = obj
        self.deadline = time_now() + datetime.timedelta(seconds=time_alived)

    def get(self):
        now = time_now()
        if now > self.deadline:
            return None
        return self.value

    def update(self, value):
        self.value = value
