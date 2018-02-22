from collections import defaultdict

# O(nW) time; O(W) space
def best(W, items):
    back = defaultdict(lambda : -1)
    
    def _best(x, opt=defaultdict(int)):
        if x in opt:
            return opt[x]
        for i, (w, v) in enumerate(items):
            if x >= w:
                ans = _best(x-w) + v
                if ans > opt[x]:
                    opt[x] = ans
                    back[x] = i
        return opt[x]

    return _best(W), solution(W, back, items)

def solution(x, back, items):
    if back[x] == -1:
        return [0] * len(items)
    w, _ = items[back[x]]
    a = solution(x-w, back, items)
    a[back[x]] += 1
    return a

def best2(W, items):
    back = defaultdict(lambda : -1)
    opt=defaultdict(int)

    for x in range(1, W+1):
        for i, (w, v) in enumerate(items):
            if x >= w:
                ans = opt[x-w] + v
                if ans > opt[x]:
                    opt[x] = ans
                    back[x] = i

    return opt[W], solution(W, back, items)

print(best(3, [(2, 4), (3, 5)]))
print(best(3, [(1, 5), (1, 5)]))
print(best(3, [(1, 2), (1, 5)]))
print(best(3, [(1, 2), (2, 5)]))

from random import randint
for _ in range(10000):
    a = [(randint(1,10), randint(1,20)) for _ in range(5)]
    X = randint(1,100)
    s, lst = best(X, a)
    if min(lst) > 0:
        print((X, a))
        print((s, lst))

print(best2(3, [(2, 4), (3, 5)]))
print(best2(3, [(1, 5), (1, 5)]))
print(best2(3, [(1, 2), (1, 5)]))
print(best2(3, [(1, 2), (2, 5)]))
print(best(11, [(2, 12), (4, 25), (3, 20)]))
