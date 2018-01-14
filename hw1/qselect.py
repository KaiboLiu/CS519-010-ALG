def qselect(a,k):  
    if len(a)<k:return a  
    pivot = a[-1]  
    right = [pivot] + [x for x in a[:-1] if x>=pivot]  
    rlen = len(right)  
    if rlen==k:  
        return right  
    if rlen>k:  
        return qselect(right, k)  
    else:  
        left = [x for x in a[:-1] if x<pivot]  
        return qselect(left, k-rlen) + right  
  
for i in range(1, 10):  
    print('k =',i, qselect([11,8,4,1,5,2,7,9], i))