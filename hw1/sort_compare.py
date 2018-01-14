from time import time
from random import randint
def qsort1(a):
    if a == []:
        return []
    else:
        pivot = a[0]
        left = [x for x in a if x < pivot]
        right = [x for x in a[1:] if x >= pivot]
        return qsort1(left) + [pivot] + qsort1(right)

def qsort(a):
    if a == []:
        return []
    else:
        pidx = randint(0,len(a)-1)
        a[0], a[pidx] = a[pidx], a[0]
        pivot = a[0]
        left = [x for x in a if x < pivot]
        right = [x for x in a[1:] if x >= pivot]
        return qsort(left) + [pivot] + qsort(right)
def sort_go(a):
    start_time = time()
    b = qsort1(a)
    print('fixed pivot, time: %s' % (time()-start_time))
    start_time = time()
    b = qsort(a)
    print('random pivot, time: %s' % (time()-start_time))
    start_time = time()
    b = sorted(a)
    print('default sort, time: %s' % (time()-start_time))
    return b