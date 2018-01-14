import sys
from sort_compare import *
from random import shuffle

sys.setrecursionlimit(100000)
a = range(10000)
print('list a =', a)
a = list(a)
b = sort_go(a)
shuffle(a)
print('sort after shuffle a:')
b = sort_go(a)
