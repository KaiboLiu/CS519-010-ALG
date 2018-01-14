from random import randint

#def sorted(t): returns the sorted order (infix traversal)
#def search(t, x): returns whether x is in t
#def insert(t, x): inserts x into t (in-place) if it is missing, otherwise does nothing.

def qsort(a):
    if a == []: return []
    #pidx = randint(0,len(a)-1)
    #a[0], a[pidx] = a[pidx], a[0]      
    pivot = a[0]    # fixed pivot at the first element
    left  = [x for x in a if x < pivot]
    right = [x for x in a[1:] if x >= pivot]
    return [qsort(left)] + [pivot] + [qsort(right)]

def qselect(k,a):
    if k > len(a): k = len(a)
    if k < 1: k = 1
    b = qselect_sort(k,a)
    return b[-1]


a = [11,8,5,1,5,2,7,9]
print(sorted(a))
print(a)  
print('sorted', qsort(a))
