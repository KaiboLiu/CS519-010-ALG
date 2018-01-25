# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 23:10:44 2018
@author: Kaibo Liu
"""
from random import randint

def qselect_sort(k,a):
    if len(a) < k: return a
    pidx = randint(0,len(a)-1)
    a[0], a[pidx] = a[pidx], a[0]
    pivot = a[0]
    left = [x for x in a[1:] if x<pivot] + [pivot]
    llen = len(left)
    if llen == k:
        return left
    if llen > k:
        return qselect_sort(k,left)
    else:
        right = [x for x in a[1:] if x>=pivot]
        return left + qselect_sort(k-llen,right)

        
#### remove redundant entries from the end whose dif == c[-1]         
def find(a, x, k):
    b = [abs(v-x) for v in a]
    c = qselect_sort(k, b)

    res = [v for v in a if abs(v-x) <= c[-1]]  # c[-1] is the threshold
    pos = len(res) - 1
    while len(res) > k:
        while abs(res[pos]-x) < c[-1]:
            pos = pos - 1
        res.pop(pos)
        pos = pos - 1
    return res

#### add necessary entries from the beginning whose dif == c[-1]        
def find2(a, x, k):
    b = [abs(v-x) for v in a]
    c = qselect_sort(k, b)
    n_less = sum(1 for v in a if abs(v-x) < c[-1])  # c[-1] is the threshold
    count, target = 0, k - n_less                   # number of entries added to result whose dif == thresholds 

    res  = []
    for v in a:
        if abs(v-x) == c[-1] and count < target:
            res.append(v)
            count = count + 1
        elif abs(v-x) < c[-1]:
            res.append(v)
    return res, n_less


    
from time import time

if __name__ == "__main__":
    print(find([4,1,3,2,7,4], 5.2, 2))      # >>[4, 4]
    print(find([4,1,3,2,7,4], 6.5, 3))      # >>[4, 7, 4]
    print(find([4,4,4,4,4,1,3,2,7,4], 6.5, 3))  # >>[4, 4, 7]
    print(find([5,3,4,1,6,3], 3.5, 2))      # >>[3, 4]
    
    #### test to compare find() and find2()
    '''
    x_max = 10000
    step = 100000
    for n in range(step,step*10,step):
        a = [randint(0,x_max) for i in range(n)]
        x = randint(0,x_max)
        k = randint(1,n)
        #k = int(n*7/10)
        
        t = time()
        res2,n_less = find2(a,x,k)
        t2 = time() - t
        print('N=%d, k=%d, n_threshold=%d' % (n, k,k-n_less))
        t = time()
        res1 = find(a,x,k)
        print('---Method1 (remove threshold), t=%f' % (time()-t)) 
        print('---Method2 (add threshold ->), t=%f' % (t2))

        diff = 0
        for i in range(k):
            if res1[i] != res2[i]: diff = diff + 1
        if diff > 0:
            print(diff)
    '''


