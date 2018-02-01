# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 00:05:58 2018
@author: Kaibo Liu
"""

def find(a):
    res = []
    a.sort()
    for z in a:
        i, j= 0, len(a)-1
        while i < j:
            while i < j and a[i]+a[j] < z: i = i+1
            while i < j and a[i]+a[j] > z: j = j-1
            if a[i] == z: i = i + 1
            if a[j] == z: j = j - 1
            if i < j and a[i]+a[j] == z:
                res.append((a[i],a[j],z))
                i = i + 1
                j = j - 1
    return res
    
def find2(a,t): # find pair (x,y) if x+y==v
    res = []
    half = t/2
    a.sort()
    x = {i:1 for i in a}
    for i in a:
        if i > half : continue
        if t-i in x:
            res.append((i,t-i))
    return res



from random import randint

if __name__ == "__main__":
    '''
    a = [1,4,2,3,5]
    print(find([1,4,2,3,5]))
    print(find([1,-4,0,-3,-1]))
    print(find([1,-4,0,-3,-1,-2,3,4,5]))
    print(find2([1,-4,0,-3,-1,-2,3,4,5],0))
    '''
    a = [randint(-10,20) for i in range(50)]
    print(sorted(a))    
    print(find3(a))


