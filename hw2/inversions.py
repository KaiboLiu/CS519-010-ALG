def mergesort_inv(a):
    if len(a) <= 1: return a, 0
    mid      = int(len(a) / 2)
    left  = mergesort_inv(a[:mid])
    right = mergesort_inv(a[mid:])
    b = merge_inv(left[0],right[0])
    return b[0], b[1] + left[1] + right[1]


def merge_inv(a,b):
    i, j, c, n_inv = 0, 0, [], 0
    lenA = len(a)
    while i < lenA and j < len(b):
        if a[i] <= b[j]:
            c.append(a[i])
            i += 1
        else: 
            c.append(b[j])
            j += 1
            n_inv += lenA - i
    c[len(c):len(c)] = a[i:] if i < len(a) else b[j:]
    return c, n_inv

def num_inversions(a):
    return mergesort_inv(a)[1]


import bisect
def num_inversions2(a):
    b, n = [], 0
    for x in a:
        idx = bisect.bisect(b, x)
        n += len(b)-idx
        b.insert(idx, x)
    return n

def num_inversions3(a):
    b, n = [], 0
    for x in reversed(a):
        idx = bisect.bisect_left(b, x)
        n += idx
        b.insert(idx, x)
    return n


if __name__ == "__main__":
    print('num_inversions([4, 1, 3, 2])')
    print(num_inversions([4, 1, 3, 2]))


    print('num_inversions([2, 4, 1, 3])')
    print(num_inversions([2, 4, 1, 3]))

    print('num_inversions([1, 2, 3, 4])')
    print(num_inversions([1, 2, 3, 4]))
    
    print('num_inversions([4, 3, 2, 1])')
    print(num_inversions([4, 3, 2, 1]))    

    print('num_inversions(range(100,0,-1))')
    print(num_inversions(list(range(100,0,-1))))

    from random import randint, seed
    import time
    N = 10000
    SEED = 2
    seed(SEED); a = [randint(0,N) for _ in range(N)]
    t0 = time.time()
    print('mergesort, {0}, time: {1:.3f}s'.format(num_inversions(a), time.time()-t0))

    seed(SEED); a = [randint(0,N) for _ in range(N)]
    t0 = time.time()
    print('bisect,    {0}, time: {1:.3f}s'.format(num_inversions2(a), time.time()-t0))

    seed(SEED); a = [randint(0,N) for _ in range(N)]
    t0 = time.time()
    print('bisect,    {0}, time: {1:.3f}s'.format(num_inversions3(a), time.time()-t0))

