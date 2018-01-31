## hw1 qselect with key
from random import randint
def qselect(k, a, key = lambda x:x):
    if a == [] or k < 1 or k > len(a):
        return None
    else:
        pindex = randint(0, len(a)-1)
        a[0],a[pindex] = a[pindex],a[0]
        pivot = a[0]
        left = [x for x in a if key(x) < key(pivot)]
        right = [x for x in a[1:] if key(x) >= key(pivot)]
        lleft = len(left)
        return pivot if k == lleft+1 else \
            qselect(k, left,key) if k <= lleft else \
            qselect(k-lleft-1, right,key)
## end
import heapq
mykey = lambda x: (x[0]+x[1], x[1])

def nbesta(a, b):
    c = [(x,y) for x in a for y in b]
    c.sort(key = mykey)
    return c[:len(a)]

def nbestb(a, b):
    c = [(x,y) for x in a for y in b]
    result = [qselect(i,list(c),mykey) for i in range(1, len(a)+1)]
    return result

def nbestc(a, b):
    if len(a) == []:
        return []
    sa, sb = sorted(a), sorted(b)
    l, result = len(a), []
    h, ifused = [], set()

    heapq.heappush(h, (mykey((sa[0],sb[0])), (0,0)))
    while len(result) < l:
        i,j = heapq.heappop(h)[1]
        result.append((sa[i],sb[j]))
        if i+1<l and (i+1,j) not in ifused:
            heapq.heappush(h, (mykey((sa[i+1],sb[j])), (i+1,j)))
            ifused.add((i+1,j))
        if j+1<l and (i,j+1) not in ifused:
            heapq.heappush(h, (mykey((sa[i],sb[j+1])), (i,j+1)))
            ifused.add((i,j+1))
    return result

if __name__ == "__main__":

    from time import time
    N = 200
    vMax = 100000
    a = [randint(0,vMax) for i in range(N)]
    b = [randint(0,vMax) for i in range(N)]

    time1 = time()
    resa = nbesta(a, b)   # algorithm (a), slowest
    print(('nbest (a), with n=%d, time=%f' %(N, time()-time1)))

    time1 = time()
    resb = nbestb(a, b)   # algorithm (b), slow
    print(('nbest (b), with n=%d, time=%f' %(N, time()-time1)))

    time1 = time()
    resc = nbestc(a, b)   # algorithm (c), fast
    print(('nbest (c), with n=%d, time=%f' %(N, time()-time1)))

    diffb = [i for i in range(N) if resa[i] != resb[i]]
    diffc = [i for i in range(N) if resa[i] != resc[i]]
    #print(resa)
    #print(resb)
    #print(resc)
    if diffb == [] and diffc == []:
        print('same result')
    elif diffb != []:
        print(('a,b: ',diffb))
    elif diffc != []:
        print(('a,c: ',diffc))