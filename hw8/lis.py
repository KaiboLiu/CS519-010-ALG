
# lis1: O(n^2) time and O(n) space
def lis2(s):
    l = len(s)
    f = [0]*l
    f[0] = 1
    for j in range(1,l):
        for i in range(j):
            if s[i] < s[j] and f[i] > f[j]:
                f[j] = f[i]
        f[j] += 1
    j = f.index(max(f)) # better to add an inf at the end to avoid searching for the max
    res = s[j]
    while j > 0 and f[j] > 1:
        i = j - 1
        while True:
            if i < 0: break
            if s[i] < s[j] and f[i] == f[j]-1:
                res += s[i]
                j = i
                break
            i -= 1
    return res[::-1]


# lis: O(nlogn) time and O(n) space (although I used a list of lists)
import bisect
def lis(s):     # pos is the index in s, idx is the index in f[i], f[i] is the the min ending value for a i-length Lis
    if len(s) < 2: return s
    f, history = [], []
    for pos, ch in enumerate(s):
        idx = bisect.bisect_left(f,ch)
        if idx >= len(f): 
            f.append(ch)
            history.append([pos])
        elif f[idx] != ch: 
            f[idx] = ch
            history[idx].append(pos)

    res, idx = '', len(s)
    for l in history[::-1]:
        while l[-1] >= idx:
            l.pop()
        res += s[l[-1]]
        idx = l[-1]
    return res[::-1]#len(f)


if __name__ == "__main__":
    
    print(lis("aebbcg"))
    ##"abcg"
    print(lis("aebabdgc"))
    ##"abdg"
    print(lis("zyx"))
    ##"z"
    

    import time
    from random import randint,seed
    seed(10)   #random.seed
    cases = 5
    for i in range(cases):
        l = randint(10,10000)
        s = [chr(randint(0,25)+ord('a')) for _ in range(l)]
        s = ''.join(s)
        time0 = time.time()
        res = lis(s)
        time1 = time.time()
        res2 = lis2(s)
        time2 = time.time()
         
        if len(res) != len(res2): print('not same value\n%s\n%s' %(res, res2))
        
        print('len=%d len_res=%s \nbottom-up: %0.5fs\ntop-down: %0.5fs'%(l,len(res),time1-time0, time2-time1))
   

