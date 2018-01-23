# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 01:10:44 2018
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
        
        

def find(a, x, k):
    b = [abs(v-x) for v in a]
    c = qselect_sort(k, b)
    res = [v for v in a if abs(v-x) <= c[-1]]  # c[-1] is the threshold
    #print('>>',res,c[-1])
    pos = len(res) - 1
    while len(res) > k:
        while abs(res[pos]-x) < c[-1]:
            pos = pos - 1
        res.pop(pos)
        pos = pos - 1
    return res
    

if __name__ == "__main__":
    
    print(find([4,1,3,2,7,4], 5.2, 2))      # >>[4, 4]
    print(find([4,1,3,2,7,4], 6.5, 3))      # >>[4, 7, 4]
    print(find([4,4,4,4,4,1,3,2,7,4], 6.5, 3))  # >>[4, 4, 7]
    print(find([5,3,4,1,6,3], 3.5, 2))      # >>[3, 4]