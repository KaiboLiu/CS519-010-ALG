from fractions import gcd
from functools import reduce
from copy import deepcopy

# O(nWlogc), binary presentation for each c[i]
def best(weight, a): # a[i] is in the form of (w_i, v_i, c_i)
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


if __name__ == "__main__":
    
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