def TD(a,i,f):
    if i < 0: return 0
    return max(a[i]+TD(a,i-2), TD(a,i-1))

    
def max_wis(a):
    


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

    print(max_wis([7,8,5]))
    ##(12, [7,5])
    print(max_wis([-1,8,10]))
    ##(10, [10])
    print(max_wis([]))
    ##(0, [])
    print(max_wis([-3,-5,-7,-9,0]))
    ##(0, [0])
    print(max_wis([-3,-5,-7,-9]))
    ##(0, [])