from random import randint

def qselect_sort(k,a):
    if len(a) < k: return a
    pidx = randint(0,len(a)-1)
    a[0], a[pidx] = a[pidx], a[0]
    pivot = a[0]
    left = [x for x in a if x<pivot] + [pivot]
    llen = len(left)
    if llen == k:
        return left
    if llen > k:
        return qselect_sort(k,left)
    else:
        right = [x for x in a[1:] if x>=pivot]
        return left + qselect_sort(k-llen,right)

def qselect(k,a):
    if k > len(a): k = len(a)
    if k < 1: k = 1
    b = qselect_sort(k,a)
    return b[-1]
'''

a = [11,8,5,1,5,2,7,5]
print(sorted(a))
print(a)  
for i in range(0,10):  
    #print('k =',i, qselect(i,[11,8,4,1,5,2,7,9]))

    print('k =',i, qselect(i,[11,8,5,1,5,2,7,5]))
'''