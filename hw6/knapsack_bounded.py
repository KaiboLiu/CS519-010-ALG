from fractions import gcd
from functools import reduce
from collections import defaultdict


'''
# bottom-up, O(nWlogc), binary presentation for each c[i]
def best(weight, a): # a[i] is in the form of (w_i, v_i, c_i)
    from copy import deepcopy
    #b = remove_redun(a)
    fac, weight, b = resize(weight,a)   # Pruning 2: Resize the capacity W, divided by gcd
    #f = {0: 0}
    f, l = [0]*(weight+1), [[0]*len(a) for _ in range(weight+1)]  # cannot use [[0]*len(a)]*(weight+1)
    for i, item in enumerate(b):
        w_i, v_i, c_i = item
        k, rest = 1, c_i-1
        while k <= c_i:
            mul = k if rest >= 0 else rest+k
            #print((w_i, v_i, c_i),mul,k,rest)
            # now we have a new item (mul*w_i, mul*v_i, 1)
            new_w = mul * w_i
            for w in range(weight,new_w-1,-1):
                if f[w - new_w] + mul*v_i > f[w]:
                    f[w] = f[w - new_w] + mul*v_i
                    l[w] = deepcopy(l[w - new_w])
                    l[w][i] += mul
            #print((w_i, v_i, c_i),mul,f[weight])
            k <<= 1
            rest -= k
            
    return f[weight],l[weight]

'''
# O(nWlogc), binary presentation for each c[i]
def best(weight, a): # a[i] is in the form of (w_i, v_i, c_i)
    #b = remove_redun(a)
    fac, weight, b = resize(weight,a)   # Pruning 2: Resize the capacity W, divided by gcd
    #f = {0: 0}
    f = defaultdict(int)    # cannot use [[0]*len(a)]*(weight+1)
    prev = defaultdict(lambda:(-1,0))
    j = -1
    for i, (w_i, v_i, c_i) in enumerate(b):
        k, rest = 1, c_i-1
        while k <= c_i:
            copies = k if rest >= 0 else rest+k
            #print((w_i, v_i, c_i),copies,k,rest)
            # now we have a new item (copies*w_i, copies*v_i, 1)
            new_w = copies * w_i
            j += 1
#            for w in range(weight,new_w-1,-1):
#                if f[w - new_w] + copies*v_i > f[w]:
#                    f[w] = f[w - new_w] + copies*v_i
#                    prev[w] = i, copies, f[w]       # index of backtrack will be covered by this i
            for w in range(new_w,weight+1):
                if f[j-1, w - new_w] + copies*v_i > f[j, w]:
                    f[j, w] = f[j-1,w - new_w] + copies*v_i
                    prev[w] = i, copies, f[j, w]       # index of backtrack will be covered by this i
            #print((w_i, v_i, c_i),copies,f[weight])
            print(i,'(',w_i, v_i, c_i,')*',copies,j)
            #print(prev)
            k <<= 1
            rest -= k 
    vv = 0
    for value in f.values(): vv = max(vv, value)
    print(vv)
    return f[j,weight], backtrack(weight, prev, b)

def backtrack(w, prev, a):
    if prev[w][0] == -1:
        return [0] * len(a)
    i, copies,_ = prev[w]
    w1, _, _ = a[i]
    l = backtrack(w-w1*copies, prev, a)
    l[i] += copies 
    return l





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
        b = [(x[0]//fac, x[1], x[2]) for x in a]
        weight = weight // fac
    else: b = a
    return fac, weight, b




# O(Wn') time where n'=sum_i c_i; O(Wn) space
def best2(W, items):
    n = len(items)
    back = defaultdict(int)

    def _best(x, i, opt=defaultdict(int)):
        if i < 0 or (x, i) in opt:
            return opt[x, i]
        w, v, c = items[i]
        xx = x
        for j in range(c+1): # take 0..c copies of item_i
            if xx < 0: # empty bag
                break
            ans = _best(xx, i-1) + v * j
            if ans > opt[x, i]:
                opt[x, i] = ans
                back[x, i] = j
            xx -= w
        return opt[x, i]

    return _best(W, n-1), solution(W, n-1, back, items)

def solution(x, i, back, items):
    if i < 0:
        return []
    j = back[x, i]
    w, _, _ = items[i]
    return solution(x - w*j, i-1, back, items) + [j]

'''
def best(W, items):
    back = defaultdict(int)
    opt = defaultdict(int)
    n = len(items)
    
    for x in range(1, W+1):
        for i in range(n):
            w, v, c = items[i]
            xx = x
            for j in range(c+1): # take 0..c copies of item_i
                if xx < 0: # empty bag
                    break
                ans = opt[xx, i-1] + v * j
                if ans > opt[x, i]:
                    opt[x, i] = ans
                    back[x, i] = j
                xx -= w

    return opt[W, n-1], solution(W, n-1, back, items)

'''

if __name__ == "__main__":
    '''
    print(best(3, [(2, 4, 2), (3, 5, 3)]))
    ##(5, [0, 1])
    print(best(3, [(1, 5, 2), (1, 5, 3)]))
    ##(15, [2, 1])
    print(best(3, [(1, 5, 1), (1, 5, 3)]))
    ##(15, [1, 2])
    print(best(20, [(1, 10, 6), (3, 15, 4), (2, 10, 3)]))
    ##(130, [6, 4, 1])
    print(best(92, [(1, 6, 6), (6, 15, 7), (8, 9, 8), (2, 4, 7), (2, 20, 2)]))
    ##(236, [6, 7, 3, 7, 2])
    '''
    print(best(92, [(1, 6, 6), (6, 15, 7), (8, 9, 8), (2, 4, 7), (2, 20, 2)]))
    ##(236, [6, 7, 3, 7, 2])
    '''
    import time
    from random import randint,seed
    seed(100)   #random.seed
    cases = 5
    for i in range(cases):
        weight = randint(10,1000)
        n = randint(10,1000)
        item = [(randint(10,100), randint(1,100), randint(1,100)) for _ in range(n)]
        if i == 0:
            n, weight, item = 5, 92, [(1, 6, 6), (6, 15, 7), (8, 9, 8), (2, 4, 7), (2, 20, 2)]
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
    '''