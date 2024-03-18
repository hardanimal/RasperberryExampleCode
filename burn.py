# encoding: utf-8

__author__ = 'Danzel.Li'

import os
import _thread
from multiprocessing import Process

def foo():
    while(True):
        i = 1 + 1

if __name__ == "__main__":
    cpu = os.cpu_count()
    for i in range(cpu):
        p = Process(target = foo, args = ())
        p.start()

    input()
