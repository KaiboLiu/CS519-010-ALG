active
s[i] = sum (a[0]..a[i]) # sum from a[0] to a[i]
or
s[i] = a[i-1]+s[j]
for i,j
    res = max(s[j]-s[i])






n = len(a)
s = {-1:0}

for i in range(n): s[i] = s[i-1]+a[i]  # s[i] is the sum from a[0] to a[i]
res = 0
for i in range(-1,n-1):
     for j in range(i+1,n)
        res = max(s[j]-s[i])    # s[j]-s[i] is the sum (a[i]..a[j])



is a removed one can be inserted again?



class oop():
    a = []                          # a来存val，顺序无所谓，下标存在idx中
    idx = defaultdict(lambda:-1)    # -1为不存在， >=0为存在, idx[val]为val在a中的位置
    n = 0
    get_rand = 0
                            #a[id] = val,
                            #idx[val] = id

    def insert(val): 
        if idx[val] >= 0: return "existed"
        idx[val] = len(a)
        a.append(val)
        n += 1
        #removed[idx[val]] = False

    def remove(val):
        if idx[val] < 0: return "not existed"
        idx[val] = -1
        #removed[idx[val]] = True

    def getRandom():




a.index(val) is O(n)





