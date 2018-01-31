import itertools
from random import randint


key1 = lambda p: (p[0]+p[1], p[1])

def nbesta(a,b):
    c = list(itertools.product(a,b))
    c.sort(key = key1)         # cmp no longer exists in python3
    return c[:len(a)]


def nbestb(a,b):
    n = len(a)
    c = list(itertools.product(a,b))
    return qselect_list(len(a),c)


def nbestc(a,b):

heapq.heappush(h, (mykey((sa[0],sb[0])), (0,0)))



def qselect_list(k,a):
    n = len(a)
    if n < k: return a
    pidx = randint(0,n-1)
    a[0], a[pidx] = a[pidx], a[0]
    pivot = a[0]

    left = [p for p in a if key1(p) < key1(pivot)]
    llen = len(left)
    if llen == k-1:
        return left + [a[0]]
    if llen > k-1:
        return qselect(k,left)
    right = [p for p in a[1:] if key1(p) >= key1(pivot)]
    return left + [a[0]] + qselect(k-llen-1,right)

if __name__ == "__main__":
    a, b = [4, 1, 5, 3], [2, 6, 3, 4]
    #a, b = [1,2,3,4], [5,6,7,8]
    print(nbesta(a, b))   # algorithm (a), slowest
    #[(1, 2), (1, 3), (3, 2), (1, 4)]
    
    print(nbestb(a, b))   # algorithm (b), slow
    #[(1, 2), (1, 3), (3, 2), (1, 4)]

    #print(nbestc(a, b))   # algorithm (c), fast
    #[(1, 2), (1, 3), (3, 2), (1, 4)]