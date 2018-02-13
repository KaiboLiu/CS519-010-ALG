#!/usr/bin/python
import random
random.seed(10)
from heapq import merge, heapify, heappop, heappush, heapreplace

def mymerge(k_lists):
    heap = [(a[0], i, 0) for i, a in enumerate(k_lists)]
    heapify(heap)
    while heap != []:
        x, i, j = heappop(heap)
        yield x
        a = k_lists[i]
        if j < len(a) - 1:
            heappush(heap, (a[j+1], i, j+1))

def mymerge2(k_lists):
    heap = [(next(a), i, a) for i, a in enumerate(map(iter, k_lists))]  # have to include i otherwise list_iterator will be compared for tie-breaking
    heapify(heap)
    while heap != []:
        x, i, a = heap[0]
        yield x
        try:
            heapreplace(heap, (next(a), i, a))
        except StopIteration: # no more elements in this sublist
            heappop(heap)

def mymerge3(k_lists):
    heap = [(next(a), i, a.__next__) for i, a in enumerate(map(iter, k_lists))] # passing the next function instead of iterator
    heapify(heap)
    while heap != []:
        x, i, next_f = heap[0]
        yield x
        try:
            heapreplace(heap, (next_f(), i, next_f))
        except StopIteration: # no more elements in this sublist
            heappop(heap)
        
def kmergesort(m, k=2):
    length = len(m)
    if length <= 1:
        return m
    split = (length-1)//k + 1
    k_lists = [kmergesort(m[i:i+split],k) for i in range(0, length, split)] # no empty sublists
    return list(merge(*k_lists))
    #return list(mymerge(k_lists))
    #return list(mymerge2(k_lists))
    #return list(mymerge3(k_lists))

if __name__ == "__main__":
    #print(kmergesort([4,1,5,2,6,3,7,0], 3))
    #print(kmergesort([random.randint(0,100) for _ in range(5)], 3))
    l = [random.randint(0,100) for _ in range(20)]
    for k in range(2, 25):
        print("k=", k, kmergesort(l, k)) 

