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
    i, count, l = j - 1, 0, len(a)
    #diff_l, diff_r = abs(a[i]-x), abs(a[j]-x)
    while (count < k):
        if (j == l):
            return a[-k:]
        if (i == 0):
            return a[:k]
        #if (diff_l <= diff_r):
        if (abs(a[i]-x) <= abs(a[j]-x)):
            i = i - 1
            #diff_l = abs(a[i]-x)
        else:
            j = j + 1
            #diff_r = abs(a[j]-x)
        count = count + 1
    
    return a[i+1:j]
    
if __name__ == "__main__":

    print(find([1,2,3,4,4,7], 5.2, 2))
    print(find([1,2,3,4,4,7], 6.5, 2))
    print(find([1,2,3,4,4,4,4,4,7], 6.5, 3))
    print(find([1,2,3,4,4,6,6], 5, 3))
    print(find([1,2,3,4,4,5,6], 4, 5))
    print(find([1,2,3,4,4,5,6], 3.9, 3))
