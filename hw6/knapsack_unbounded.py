from fractions import gcd
from functools import reduce
from collections import defaultdict
import sys

# bottom-up
def best(weight, a): # a[i] is in the form of (w_i, v_i)
    #b = remove_redun(a)
    fac, weight, b = resize(weight,a)   # Pruning 2: Resize the capacity W, divided by gcd

    f, l = [0]*(weight+1), [0]*len(a)
    for w_i, v_i in b:
        for w in range(w_i,weight+1):
            #if w >= w_i:
            f[w] = max( f[w], f[w-w_i]+v_i )
    W = weight
    for i, item in enumerate(b):
        while W >= item[0] and f[W]-f[W-item[0]] == item[1]:
            l[i] += 1
            W -= item[0]
    return f[weight],l


# top-down
def best2(weight, a):   
    sys.setrecursionlimit(100000)
    prev = defaultdict(lambda:-1)
    fac, weight, b = resize(weight,a)   # Pruning 2: Resize the capacity W, divided by gcd

    def sub(W, f=defaultdict(int)):
        if W in f: return f[W]
        for i, (w_i,v_i) in enumerate(b):
            if W >= w_i:
                V = sub(W-w_i) + v_i
                if V > f[W]:
                    f[W] = V
                    prev[W] = i
        return f[W]

    return sub(weight), backtrack(weight, prev, b)

def backtrack(w, prev, a):
    if prev[w] == -1:
        return [0] * len(a)
    w1, _= a[prev[w]]
    l = backtrack(w-w1, prev, a)
    l[prev[w]] += 1
    return l

'''

# Pruning 1: delete redundent items
# no way to delete redundent item with larger w and smaller v, because we need the list of copies chosen with original index
def remove_redun(a):    
    s, b, i= sorted(a), [], 0
    length = len(a)
    while i < length:
        while i < length-1 and s[i][0]==s[i+1][0]: i += 1
        b.append(s[i])
        j = i + 1
        while j < length and s[i][1] >= s[j][1]: j += 1
        i, j = j, j+1
    return b
    

# Pruning 2: Resize the capacity W, divided by gcd
# use gcd(Greatest Common Divisor) in w to trim the size of weight to weight/gcd
def resize(weight, a):
    fac = reduce(gcd,[x[0] for x in a]+[weight])
    if fac > 1:
        b = [(x[0]//fac, x[1]) for x in a]
        weight = weight // fac
    else: b = a
    return fac,weight, b
'''

if __name__ == "__main__":
    print(best(6, [(4, 4), (6, 5)]))
    print(best(3, [(2, 4), (3, 5)]))
    ## (5, [0, 1])
    print(best(3, [(1, 5), (1, 5)]))
    ## (15, [3, 0])
    print(best(3, [(1, 2), (1, 5)]))
    ## (15, [0, 3])
    print(best(3, [(1, 2), (2, 5)]))
    ## (7, [1, 1])
    print(best(58, [(5, 9), (9, 18), (6, 12)]))
    ## (114, [2, 4, 2])
    print(best(92, [(8, 9), (9, 10), (10, 12), (5, 6)]))
    ## (109, [1, 1, 7, 1])
    

    import time
    from random import randint,seed
    seed(100)   #random.seed
    cases = 5
    for i in range(cases):
        weight = randint(10,10000)
        n = randint(10,1000)
        item = [(randint(10,100), randint(1,100)) for _ in range(n)]
        time0 = time.time()
        res = best(weight, item)
        time1 = time.time()
        res2 = best2(weight, item)
        time2 = time.time()
        if res[0] != res2[0]: print('not same value')
        for j in range(n):
            if res[1][j] != res2[1][j]:
                print('not same distribution')
                break
        print('W={} n={}\nbottom-up: {}s\ntop-down: {}s'.format(weight,n,time1-time0, time2-time1))

