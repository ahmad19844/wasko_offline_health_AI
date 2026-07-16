"""
utils.py
"""

import time


def timer():

    return time.perf_counter()


def elapsed(start):

    return round(

        time.perf_counter() - start,

        3

    )


def format_seconds(seconds):

    return f"{seconds:.2f} sec"
