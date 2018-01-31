from random import randint

def qselect(k,a):
    if len(a) < k: return a
    pidx = randint(0,len(a)-1)
    a[0], a[pidx] = a[pidx], a[0]
    pivot = a[0]
    left = [x for x in a if x < pivot]
    llen = len(left)
    if llen == k-1:
        return pivot
    if llen > k-1:
        return qselect_sort(k,left)
    else:
        right = [x for x in a[1:] if x >= pivot]
        return qselect_sort(k-llen-1,right)

'''

a = [11,8,5,1,5,2,7,5]
print(sorted(a))
print(a)  
for i in range(0,10):  
    #print('k =',i, qselect(i,[11,8,4,1,5,2,7,9]))

    print('k =',i, qselect(i,[11,8,5,1,5,2,7,5]))
'''