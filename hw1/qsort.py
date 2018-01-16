from random import randint

def sorted(t):
    if t == []: return []
    return sorted(t[0]) + [t[1]] + sorted(t[2])

def _search(t, x):
    if t == []: return t
    if (x == t[1]):
        return t
    elif (x < t[1]):
        return _search(t[0],x)
    else:
        return _search(t[2],x)

def search(t, x): 
    subtree = _search(t,x)
    if subtree == []: return False
    return True

def insert(t, x): 
    subtree = _search(t,x)
    if subtree == []: 
        subtree += [[], x, []]
        #subtree.append([])
        #subtree.append(x)
        #subtree.append([])
    return t

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


#a = [11,8,5,1,5,2,7,9]
a = [4,2,6,3,5,7,1,9]
print(a)  
tree = qsort(a)

print('tree', tree)
print('sorted', sorted(tree))
print('search(tree, 6)', search(tree, 6))
print('search(tree, 6.5)', search(tree, 6.5))

insert(tree, 6.5)
print('insert(tree, 6.5)', tree)
insert(tree, 3)
print('insert(tree, 3)', tree)
