# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 00:25:58 2018
@author: Kaibo Liu
"""

from bisect import bisect

def find(a, x, k):
    if len(a) <= k: 
        return a
    j = bisect(a, x)    # equals bisect_right()
    i, n, l = j - 1, 0, len(a)
    res = []
    while (n < k):
        if (j == l) or (i >= 0 and abs(a[i] - x) <= abs(a[j] - x)):
            #res.insert(0, i*100+a[i])
            res.insert(0, a[i])
            i = i - 1
        else:
            #res.append(j*100+a[j])
            res.append(a[j])
            j = j + 1
        n = n + 1
    
    return res
    
if __name__ == "__main__":
    
    print(find([1,2,3,4,4,7], 5.2, 2))
    print(find([1,2,3,4,4,7], 6.5, 3))
    print(find([1,2,3,4,4,4,4,4,7], 6.5, 3))
    print(find([1,2,3,4,4,6,6], 5, 3))
    print(find([1,2,3,4,4,5,6], 4, 5))