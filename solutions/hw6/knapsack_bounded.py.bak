from collections import defaultdict

# O(Wn') time where n'=sum_i c_i; O(Wn) space
def best(W, items):
    n = len(items)
    back = defaultdict(int)

    def _best(x, i, opt=defaultdict(int)):
        if i < 0 or (x, i) in opt:
            return opt[x, i]
        w, v, c = items[i]
        xx = x
        for j in xrange(c+1): # take 0..c copies of item_i
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

def best2(W, items):
    back = defaultdict(int)
    opt = defaultdict(int)
    n = len(items)
    
    for x in xrange(1, W+1):
        for i in xrange(n):
            w, v, c = items[i]
            xx = x
            for j in xrange(c+1): # take 0..c copies of item_i
                if xx < 0: # empty bag
                    break
                ans = opt[xx, i-1] + v * j
                if ans > opt[x, i]:
                    opt[x, i] = ans
                    back[x, i] = j
                xx -= w

    return opt[W, n-1], solution(W, n-1, back, items)

print best(3, [(2, 4, 2), (3, 5, 3)])
print best(3, [(1, 5, 2), (1, 5, 3)])
print best(3, [(1, 5, 1), (1, 5, 3)])
print best(20, [(1, 10, 6), (3, 15, 4), (2, 10, 3)])
print
print best2(3, [(2, 4, 2), (3, 5, 3)])
print best2(3, [(1, 5, 2), (1, 5, 3)])
print best2(3, [(1, 5, 1), (1, 5, 3)])
print best2(20, [(1, 10, 6), (3, 15, 4), (2, 10, 3)])

from random import randint
for _ in xrange(1000):
    a = [(randint(1,10), randint(1,20), randint(1, 10)) for _ in xrange(10)]
    X = randint(1,200)
    s, lst = best(X, a)
    if min(lst) > -1:
        print (X, a)
        print (s, lst)
