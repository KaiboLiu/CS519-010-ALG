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
        while i < j:# and a[i]<mid and a[j]>mid:
            while i < j and a[i]+a[j] < z: i = i+1
            while i < j and a[i]+a[j] > z: j = j-1
            if a[i] == z: i = i + 1
            if a[j] == z: j = j - 1
            if i < j and a[i]+a[j] == z:
                res.append((a[i],a[j],z))
                i = i + 1
                j = j - 1
    return res
    
if __name__ == "__main__":
    a = [1,4,2,3,5]
    print(find([1,4,2,3,5]))
    print(find([1,-4,0,-3,-1]))
    print(find([1,-4,0,-3,-1,-2,3,4,5]))
