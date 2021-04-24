#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 17:06:47 2021

@author: gopal
"""

# %%

from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    print('main process id:', os.getpid())
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
# %%
    
from multiprocessing import Process
import random
import time

def some_function(first, last):
    time.sleep(random.randint(1, 3))
    print(first, last)

processes = []

for m in range(1,16):
   n = m + 1
   p = Process(target=some_function, args=(m, n))
   p.start()
   processes.append(p)

for p in processes:
   p.join()
# %%
"""
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
"""
# %%