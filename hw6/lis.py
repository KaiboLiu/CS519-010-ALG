
# lis1: O(n^2) time and O(n) space
def lis1(s):
    l = len(s)
    f = [0]*l
    f[0] = 1
    for j in range(1,l):
        for i in range(j):
            if s[i] < s[j] and f[i] > f[j]:
                f[j] = f[i]
        f[j] += 1
    j = f.index(max(f))
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


# lis: O(nlogn) time and (n) space (although I used a list of lists)
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
    