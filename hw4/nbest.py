import itertools
import heapq
from random import randint


p_key = lambda pair: (pair[0]+pair[1], pair[1])

def nbesta(a,b):
    c = list(itertools.product(a,b))
    c.sort(key = p_key)         # cmp no longer exists in python3
    return c[:len(a)]


def nbestb(a,b):
    n = len(a)
    c = list(itertools.product(a,b))
    threshold = qselect(n,c)
    res = [p for p in c if p_key(p) <= p_key(threshold)]
    res.sort(key = p_key)
    return res[:n]


def nbestc(a,b):
    # BFS based priority queue + search histrory in set
    # containment opertation in set is O(1)
    n = len(a)
    if n == 0: return a
    A = sorted(a)
    B = sorted(b)

    h, p_set = [], set()
    res = []

    heapq.heappush(h, (p_key((A[0],B[0])), (0,0)))  # element in h is a pair (element[0], element[1]), compatiable with mult-key comparison 
                                                    # element[0] is the primary key, used to sort in h, element[1]/(i,j) is the index of pair
    while len(res) < n:
        i, j = heapq.heappop(h)[1]
        res.append((A[i],B[j]))
        if i+1 < n and (i+1,j) not in p_set:
            heapq.heappush(h, ( p_key((A[i+1],B[j])), (i+1,j) )) 
            p_set.add((i+1,j))
        if j+1 < n and (i,j+1) not in p_set:
            heapq.heappush(h, ( p_key((A[i],B[j+1])), (i,j+1) )) 
            p_set.add((i,j+1))
    return res

def nbestd(a,b):

    #c = list(itertools.product(a,b)). # 'tuple' object does not support item assignment
    c = [(x+y,y) for x in a for y in b]
    heapq.heapify(c)
    d = heapq.nsmallest(len(a),c)
    return [(X-y,y) for X,y in d]


def qselect(k,a):
    n = len(a)
    if n < k: return a
    pidx = randint(0,n-1)
    a[0], a[pidx] = a[pidx], a[0]
    pivot = a[0]

    left = [p for p in a if p_key(p) < p_key(pivot)]
    llen = len(left)
    if llen == k-1:
        return pivot
    if llen > k-1:
        return qselect(k,left)
    right = [p for p in a[1:] if p_key(p) >= p_key(pivot)]
    return qselect(k-llen-1,right)

if __name__ == "__main__":
    '''
    a, b = [4, 1, 5, 3], [2, 6, 3, 4]
    print(nbesta(a, b))   # algorithm (a), slowest
    #[(1, 2), (1, 3), (3, 2), (1, 4)]
    print(nbestb(a, b))   # algorithm (b), slow
    #[(1, 2), (1, 3), (3, 2), (1, 4)]
    print(nbestc(a, b))   # algorithm (c), fast
    #[(1, 2), (1, 3), (3, 2), (1, 4)]
    '''

    # large list test for time
    from time import time
    N = 1000
    vMax = 10000
    a = [randint(0,vMax) for i in range(N)]
    b = [randint(0,vMax) for i in range(N)]

    time1 = time()
    resa = nbesta(a, b)   # algorithm (a), slowest
    print('nbest (a), with n=%d, time=%f' %(N, time()-time1))

    time1 = time()
    resb = nbestb(a, b)   # algorithm (b), slow
    print('nbest (b), with n=%d, time=%f' %(N, time()-time1))

    time1 = time()
    resc = nbestc(a, b)   # algorithm (c), fast
    print('nbest (c), with n=%d, time=%f' %(N, time()-time1))

    time1 = time()
    resd = nbestd(a, b)   # algorithm (c), fast
    print('nbest (d), with n=%d, time=%f' %(N, time()-time1))

    diffb = [i for i in range(N) if resa[i] != resb[i]]
    diffc = [i for i in range(N) if resa[i] != resc[i]]
    diffd = [i for i in range(N) if resa[i] != resd[i]]
    #print(resa)
    #print(resb)
    #print(resc)
    if diffb == [] and diffc == [] and diffd == []:
        print('same results')
    if diffb != []:
        print('a,b: ',diffb)
    if diffc != []:
        print('a,c: ',diffc)
    if diffd != []:
        print('a,d: ',diffd)