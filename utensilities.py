# -*- coding: utf-8 -*-
# jvparidon@gmail.com
from time import time, localtime, strftime


def timer(func):
    """Decorator to add timing wrapper to other functions.

    Use by prepending @timer to the target function definition.
    Logs start and finish time in y/m/d h:m:s and keeps track of duration in seconds.
    Wrapper returns a tuple containing the original results and a dictionary containing start, finish, and duration.

    :param func: any function
    :return: func with timing wrapper
    """
    def timed_func(*args, **kwargs):
        t = {}
        t['start'] = strftime('%Y/%m/%d %H:%M:%S', localtime())
        t0 = time()
        res = func(*args, **kwargs)
        t1 = time()
        t['finish'] = strftime('%Y/%m/%d %H:%M:%S', localtime())
        t['duration'] = t1 - t0
        return res, t
    return timed_func
