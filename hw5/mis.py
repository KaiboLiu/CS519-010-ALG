from random import randint
import time
import sys

sys.setrecursionlimit(10000)
## Maximum Weighted Independent Set 
## [HINT] independent set is a set where no two numbers are neighbors in the original list.


## top-down, to memorize the list for each step i, in dict s
def TD(a,i,s):  # s is a dict, element is {i:(s,l)}, where s is the sum for i, and l is the list of chosen a[i]s for the optimal sum
    if i < 0: return 0,[]
    if i-1 in s:
        s1, l1 = s[i-1][0], s[i-1][1]
    else:
        s1, l1 = TD(a,i-1,s)
        s[i-1] = (s1,l1)

    if i-2 in s:
        s2, l2 = s[i-2][0], s[i-2][1]
    else: 
        s2, l2 = TD(a,i-2,s)
        s[i-2] = (s2,l2)

    if s1 <= s2+a[i]:
        s[i] = ( s2+a[i], l2+[a[i]] )
        return s[i][0],s[i][1]
    else: 
        s[i] = ( s1, l1 )
        return s1,l1

## outer function of top-down    
def max_wis(a):
    return TD(a, len(a)-1, {})


## bottom-up, linear DP for maximum sum, then backwoard to get the list
def max_wis2(a):
    l = len(a)
    f, res = {-2:0,-1:0}, []
    for i,x in enumerate(a):
        f[i] = max(f[i-1], f[i-2]+x)
    #for i,x in enumerate(a[::-1]):
    i = l-1
    while i >= 0:
        if f[i] == f[i-2]+a[i]:
            res.append(a[i])
            i = i-2
        else: i = i-1       # f[i] == f[i-1]
    return f[l-1], res[::-1]




if __name__ == "__main__":

    print(max_wis([7,8,5]), max_wis2([7,8,5]))
    ##(12, [7,5])
    print(max_wis([-1,8,10]), max_wis2([-1,8,10]))
    ##(10, [10])
    print(max_wis([]), max_wis([]))
    ##(0, [])
    print(max_wis([-3,-5,-7,-9,0]), max_wis2([-3,-5,-7,-9,0]))
    ##(0, [0])
    print(max_wis([-3,-5,-7,-9]), max_wis2([-3,-5,-7,-9]))
    ##(0, [])
    N = 4000
    a = [randint(-1000,1000) for i in range(N)]
    t0 = time.time()
    r1 = max_wis(a)
    t1 = time.time() - t0
    t0 = time.time()
    r2 = max_wis2(a)
    t2 = time.time() - t0
    if r1[0] != r2[0]: print(r1, r2)
    print(t1,t2)