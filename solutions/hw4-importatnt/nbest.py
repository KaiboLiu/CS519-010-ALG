from random import randint
import heapq

def qselect(k, a):
    if a == [] or k < 1 or k > len(a):
        return None
    else:
        pindex = randint(0, len(a)-1)
        a[0], a[pindex] = a[pindex], a[0]
        pivot = a[0]
        left = [x for x in a if x < pivot]
        right = [x for x in a[1:] if x >= pivot]
        lleft = len(left)
        return pivot if k == lleft+1 else \
            qselect(k, left) if k <= lleft else \
            qselect(k-lleft-1, right)

def nbesta(a, b):
    c = [((x+y, y), (x,y)) for x in a for y in b] # decorate
    return [xy for _, xy in sorted(c)[:len(a)]] # sort and undecorate

def nbestb(a, b):
    c = [((x+y, y), (x,y)) for x in a for y in b]
    threshold = qselect(len(a), c) 
    result = [stuff for stuff in c if stuff <= threshold]
    return [xy for _, xy in sorted(result)[:len(a)]]

def _nbestc(a, b):
    def put(i, j):
        if 0 <= i < n and 0 <= j < n and (i, j) not in used:
            used.add((i, j))
            heapq.heappush(h, ((sa[i]+sb[j], sb[j]), (sa[i], sb[j]), (i, j))) # decorate: cmp_key, pair, index
        
    sa, sb = sorted(a), sorted(b)
    n = len(a)
    h, used = [], set()

    put(0, 0)
    for _ in range(n):
        _, xy, (i, j) = heapq.heappop(h)
        yield xy
        put(i+1, j)
        put(i, j+1)

nbestc = lambda a, b: list(_nbestc(a, b))

if __name__ == "__main__":
    a, b = [4,1,5,3], [2,6,3,4]
    print(nbesta(a,b))
    print(nbestb(a,b))
    print(nbestc(a,b))
