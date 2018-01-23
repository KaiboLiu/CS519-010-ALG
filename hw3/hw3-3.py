# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 00:05:58 2018
@author: Kaibo Liu
"""

def find(a):
    res = []
    a.sort()
    for k in range (2, len(a)):
        i, j, mid = 0, k-1, a[k]/2
        while i < j and a[i]<mid and a[j]>mid:
            while i < j and a[i]+a[j] < a[k]: i = i+1
            while i < j and a[i]+a[j] > a[k]: j = j-1
            if i < j and a[i]+a[j] == a[k]:
                res.append((a[i],a[j],a[k]))
                i = i + 1
                j = j - 1
    return res
    
if __name__ == "__main__":
    a = [1,4,2,3,5]
    print(find(a))