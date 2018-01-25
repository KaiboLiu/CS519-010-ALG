# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 00:25:58 2018
@author: Kaibo Liu
"""

from bisect import bisect


def find(a, x, k):
    if len(a) <= k: 
        return a
    #if x <= a[0]:
    #    return a[:k]
    #if x >= a[-1]:
    #    return a[-k:]
    j = bisect(a, x)    # equals bisect_right()
    i, count, l = j - 1, 0, len(a)
    diff_l, diff_r = x-a[i], a[j]-x
    while (count < k):
        if diff_l <= diff_r:
        #if x-a[i] <= a[j]-x:   # if no diff memorization, time of case 10: 0.176s -> 0.245s. Nice trcik!
            i = i - 1
            if (i < 0): return a[:k]
            diff_l = x - a[i]
        else:
            j = j + 1
            if (j >= l): return a[-k:]
            diff_r = a[j] - x
        count = count + 1
    
    return a[i+1:j]
    
if __name__ == "__main__":

    print(find([1,2,3,4,4,7], 5.2, 2))
    print(find([1,2,3,4,4,7], 6.5, 2))
    print(find([1,2,3,4,4,4,4,4,7], 6.5, 3))
    print(find([1,2,3,4,4,6,6], 5, 3))
    print(find([1,2,3,4,4,5,6], 4, 5))
    print(find([1,2,3,4,4,5,6], 3.9, 3))
