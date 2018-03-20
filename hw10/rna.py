'''
Developer: Kaibo(lrushx)
Email: liukaib@oregonstate.edu
Process Time: Feb 28, 2018
'''

from collections import defaultdict
from heapq import heapify, heapreplace, heappush, heappop, nlargest
import rna_liang
import pdb

p = {'AU','UA','CG','GC','UG','GU'}

################### part1 best solution of pairing ################################################
## 3 cases: .*******, (***)*** and (******)
## trace back with recurrsion + middle point
## O(n^3) time + O(n^2) space
def best(s):
    def solution(i, j):
        if i >= j: return ""
        if mid[i,j] == i+1:     # case 1
            return "." + solution(mid[i,j], j)
        if mid[i,j] > i+1:      # case 2+3 
            return "("+solution(i+1,mid[i,j]-1)+")" + solution(mid[i,j],j)
        return "."*(j-i)        # mid < 0

    opt, mid = defaultdict(int), defaultdict(lambda:-1)
    if s == '': return 0,''
    l = len(s)
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d            
            if mid[i+1,j] >= 0:
                opt[i,j], mid[i,j] = opt[i+1,j], i+1
            for k in range(i+2,j+1):  #k = i+1..j
                if s[i]+s[k-1] in p:
                    if opt[i+1,k-1]+opt[k,j]+1 > opt[i,j]:
                        opt[i,j], mid[i,j] = opt[i+1,k-1]+opt[k,j]+1, k
            
    return opt[0,l], solution(0,l)

## trace back with recurrsion + middle point
## O(n^3) time + O(n^2) space
def best1(s):
    def solution(a,b):
        if a >= b: return ""
        if mid[a,b] == -1:
            return "("+solution(a+1,b-1)+")"
        elif mid[a,b] > 0:
            return solution(a, mid[a,b]) + solution(mid[a,b], b)
        return "."*(b-a)

    opt, mid = defaultdict(int), defaultdict(int)#(lambda:-1)
    if s == '': return 0,''
    l = len(s)
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d            
            if s[i]+s[j-1] in p:
                opt[i,j], mid[i,j] = opt[i+1,j-1] + 1, -1

            for k in range(i+1,j):  #k = i+1..j-1
                if opt[i,k]+opt[k,j] > opt[i,j]:
                    opt[i,j], mid[i,j] = opt[i,k]+opt[k,j], k
            
    return opt[0,l], solution(0,l)


## store all the local optimal strucrure strc[i,j] besides opt[i,j], no trace back
## O(n^3) time + O(n^3) space(n^2 strings with size of n)
def best2(s):
    opt, strc = defaultdict(int), defaultdict(lambda:'.')
    l = len(s)

    if l < 1: return 0,''
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d            
            if s[i]+s[j-1] in p:
                opt[i,j] = opt[i+1,j-1] + 1
                strc[i,j] = '(' + strc[i+1,j-1] + ')'
            for k in range(i+1,j):  #k = i+1..j-1
                if opt[i,k]+opt[k,j] > opt[i,j]:
                    opt[i,j] = opt[i,k]+opt[k,j]
                    strc[i,j] = strc[i,k] + strc[k,j]
            if opt[i,j] == 0:
                strc[i,j] = '.' * (j-i)
    return opt[0,l], strc[0,l]


################### part2 total number of pairs ###################################################
## 3 cases: .*******, (***)*** and (******)
## O(n^3) time + O(n^2) space
def total(s):

    opt, l = defaultdict(int), len(s)
    for i in range(l+1):
        opt[i,i], opt[i,i+1] = 1, 1 # single and empty

    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d 
            opt[i,j] += opt[i+1,j]      # case 1: .*******

            for k in range(i+2,j+1):    # case 2+3: k = i+2..j, to pair s[i] with s[k-1]
                if s[i]+s[k-1] in p:
                    opt[i,j] += opt[i+1,k-1] * opt[k,j] # case 2: (***)*** or (******)
    return opt[0,l]



################### part3 k-best solutions of pairing #############################################
## 1. O(n^3k+n^2klogk)               push all into heap
## 1.5. O(klogk*n^3),                unlazy kbest, Serial_push->maitain_heap_size->list->opt[i,j] - kbest_unlazy(s,k)
## 2_1: O(2n^3+2n^2klog(n+2k)),      unlazy kbest, BFS_push->heappop->opt[i,j]                    - kbest_alg2_heapn(s,k)
## 2_2: O(n^3+3mn^2+2n^2klog(m+2k)), unlazy kbest, BFS_push->select_k->heappop->opt[i,j]          - kbest_alg2_heapk(s,k)
##      m=min(k,n)
##          O(n^3+3kn^2+2n^2klog(3k)), if k<n
##          O(4n^3+2n^2klog(n+2k)),    if k>n
## 3. O(n^3 +nklogn),                lazy generating                                              - kbest_lazy(s,k)


## alg3: kbest(s,k)
## lazy generating
## O(n^3 + nklogn) time, O(n^2(n+k)) space
def kbest_lazy(s, k):
    def solution(i, j, a):
        if i >= j: return ""
        mid = opt[i,j][a][1]
        if mid > i+1:       # case 2+3 
            return "("+solution(i+1,mid-1,opt[i,j][a][2])+")" + solution(mid,j,opt[i,j][a][3])
        if mid == i+1:      # case 1
            return "." + solution(mid, j, opt[i,j][a][3])
        return "."*(j-i)    # mid < 0

    def put(TheNext, i, j, func = heappush):
        if (i,j,TheNext[1],TheNext[2],TheNext[3]) not in used:
            func(branch[i,j], TheNext)
            used.add((i,j,TheNext[1],TheNext[2],TheNext[3]))

    def _next(i, j, kth):
        if kth < len(opt[i,j]): return opt[i,j][kth]
        if branch[i,j] == [] or branch[i,j][0][0] == 0: return None     # no _next to expand
        n, mid, a, b = heappop(branch[i,j])
        if mid == i+1:      # case 1
            right = _next(mid,j,b+1)
            if right is not None and right[0] < 0: 
                heappush(branch[i,j],(right[0], mid, a, b+1))     
        elif mid > i+1:     # case 2+3
            left  = _next(i+1, mid-1, a+1)
            right = _next(mid, j,     b+1)                    
            if left  is not None:
                put((left[0]+opt[mid,j][b][0]-1, mid, a+1, b), i, j)
            if right is not None:
                put((opt[i+1,mid-1][a][0]+right[0]-1, mid, a, b+1), i, j)
        if branch[i,j] ==[]:                    # __important__, to generate an empty one, not None
            heappush(branch[i,j],(0,-1,0,0))
        
        opt[i,j].append(branch[i,j][0])
        return branch[i,j][0]

    l, res, used = len(s), [], set()
    kth, a, b = 0, 0, 0
    opt = defaultdict(lambda:[(0,-1,0,0)])      # list of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], reversed list, sizeof m
    branch = defaultdict(lambda:[])             # heap of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], max-heap, sizeof j-i, it is the (mid-i)th branch
                                                # every time we want to extend the next largest one from opt[i+1,mid-1] and opt[mid,j]
    if s == '': return [(0, "")]
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d 
            if opt[i+1,j][kth][1] >= 0:
                opt[i,j][kth] = (opt[i+1,j][kth][0],i+1,a,b)    # case 1: .******* mid=i+1
                branch[i,j].append(opt[i,j][kth])               # init branch 0 for [i,j]
            for mid in range(i+2,j+1): 
                if s[i]+s[mid-1] in p:                            # case 2+3: (******) mid=j, or (***)*** mid=i+2..j-1
                    tmp_n = opt[i+1,mid-1][kth][0]+opt[mid,j][kth][0]-1
                    branch[i,j].append((tmp_n, mid, a, b))        # init the rest branches for [i,j]
                    if tmp_n < opt[i,j][kth][0]:
                        opt[i,j][kth] = branch[i,j][-1]
            heapify(branch[i,j])
    # by now, we solved 1-best, stored in opt[0,l][0], solution(0,l,0)
    res.append((-opt[0,l][kth][0],solution(0,l,kth)))
    for kth in range(1,k):
        TheNext = _next(0,l,kth)    
        if TheNext is None: break
        res.append((-opt[0,l][kth][0],solution(0,l,kth)))
    return res



## alg2_1: kbest_alg2_heapn(s,k)
## unlazy kbest, BFS_push->heappop->opt[i,j]
## O(2n^3 + 2n^2klog(n+2k)) time, O(n^2(n+k)) space
def kbest_alg2_heapn(s, k):
    def solution(i, j, a):
        if i >= j: return ""
        mid = opt[i,j][a][1]
        if mid > i+1:       # case 2+3 
            return "("+solution(i+1,mid-1,opt[i,j][a][2])+")" + solution(mid,j,opt[i,j][a][3])
        if mid == i+1:      # case 1
            return "." + solution(mid, j, opt[i,j][a][3])
        return "."*(j-i)    # mid < 0

    l, res = len(s), []
    opt = defaultdict(lambda:[(0,-2,0,0)])      # list of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], reversed list, sizeof m
    if s == '': return [(0, "")]
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d            
            h = [(0,-2,0,0)]
            if opt[i+1,j][0][0] < 0:
                h.append((opt[i+1,j][0][0], i+1, 0, 0))  # 1best of case 1: .*******, j=i+1
            for mid in range(i+2,j+1):  #mid = i+2..j
                if s[i]+s[mid-1] in p:  #1best of case 2+3: (***)***
                    h.append((opt[i+1,mid-1][0][0]+opt[mid,j][0][0]-1, mid, 0, 0))
            heapify(h)  # 1 best of all the branches in heap h
            if h[0][0] == 0:    continue    # remain opt[i,j] as [(0,-2,0,0)]
            opt[i,j] = []
            used = set()
            for kth in range(k):
                opt[i,j].append(heappop(h))
                n, mid, a, b = opt[i,j][-1]
                if mid == -2: break     # the # of bests is less than k
                if mid == i+1:          # case 1
                    if b < len(opt[mid,j])-1 and opt[mid,j][b+1][0] < 0:  
                        heappush(h,(opt[mid,j][b+1][0], mid, 0, b+1))
                else:                   # case 2+3
                    a1, b1 = a+1, b+1
                    if a1 < len(opt[i+1,mid-1]) and not (mid, a1, b) in used:
                        heappush(h,(opt[i+1,mid-1][a1][0]+opt[mid,j][b][0]-1, mid, a1, b))
                        used.add((mid,a1,b))
                    if b1 < len(opt[mid,j]) and not (mid, a, b1) in used:
                        heappush(h,(opt[i+1,mid-1][a][0]+opt[mid,j][b1][0]-1, mid, a, b1))
                        used.add((mid,a,b1))
    for a, (n,_,_,_) in enumerate(opt[0,l]):
        res.append((-n,solution(0,l,a)))
            
    return res 



## alg2_2: kbest_alg2_heapk(s,k)
## unlazy kbest, BFS_push->select_k->heappop->opt[i,j]
## O(n^3+3mn^2+2n^2klog(m+2k)) time, m=min(k,n) O(n^2(n+k)) space
def kbest_alg2_heapk(s, k):
    import random
    def solution(i, j, a):
        if i >= j: return ""
        mid = opt[i,j][a][1]
        if mid > i+1:       # case 2+3 
            return "("+solution(i+1,mid-1,opt[i,j][a][2])+")" + solution(mid,j,opt[i,j][a][3])
        if mid == i+1:      # case 1
            return "." + solution(mid, j, opt[i,j][a][3])
        return "."*(j-i)    # mid < 0

    def qselect(a, k):  # smallest:k=1
        if k > len(a) or k==0 or a == []: return []
        idx = random.randint(0,len(a)-1)
        a[idx],a[0] = a[0],a[idx]
        pivot = a[0]
        left = [x for x in a if x < pivot]
        ll = len(left)
        if k == ll+1: return pivot
        if k <= ll: return qselect(left,k)
        right = [x for x in a[1:] if x >= pivot]
        return qselect(right,k-ll-1)

    def cut(a, k):  # quickselect + return all the klargest
        if k >= len(a): return a
        pivot = qselect(a, k)
        return [x for x in a if x <= pivot]


    l, res = len(s), []
    opt = defaultdict(lambda:[(0,-2,0,0)])      # list of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], reversed list, sizeof m
    if s == '': return [(0, "")]
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d            
            h = [(0,-2,0,0)]
            if opt[i+1,j][0][0] < 0:
                h.append((opt[i+1,j][0][0], i+1, 0, 0))  # 1best of case 1: .*******, j=i+1
            for mid in range(i+2,j+1):  #mid = i+2..j
                if s[i]+s[mid-1] in p:  #1best of case 2+3: (***)***
                    h.append((opt[i+1,mid-1][0][0]+opt[mid,j][0][0]-1, mid, 0, 0))
            h = cut(h,k)
            heapify(h)  # 1 best of all the branches in heap h
            if h[0][0] == 0:    continue    # remain opt[i,j] as [(0,-2,0,0)]
            opt[i,j] = []
            used = set()
            for kth in range(k):
                opt[i,j].append(heappop(h))
                n, mid, a, b = opt[i,j][-1]
                if mid == -2: break     # the # of bests is less than k
                if mid == i+1:          # case 1
                    if b < len(opt[mid,j])-1 and opt[mid,j][b+1][0] < 0:  
                        heappush(h,(opt[mid,j][b+1][0], mid, 0, b+1))
                else:                   # case 2+3
                    a1, b1 = a+1, b+1
                    if a1 < len(opt[i+1,mid-1]) and not (mid, a1, b) in used:
                        heappush(h,(opt[i+1,mid-1][a1][0]+opt[mid,j][b][0]-1, mid, a1, b))
                        used.add((mid,a1,b))
                    if b1 < len(opt[mid,j]) and not (mid, a, b1) in used:
                        heappush(h,(opt[i+1,mid-1][a][0]+opt[mid,j][b1][0]-1, mid, a, b1))
                        used.add((mid,a,b1))
    for a, (n,_,_,_) in enumerate(opt[0,l]):
        res.append((-n,solution(0,l,a)))
            
    return res 
################### part0 customized check ########################################################
def check_kbest(res, k):
    check, wrong = set(), 0
    for n,s in res: 
        check.add(s)
        if cntPairs(s) != n: wrong += 1
    return len(check)==len(res), wrong

    
## customized funtion to count pairs in a structure
def cntPairs(s):
    stack, n = [],0
    for i, item in enumerate(s):
        if item == '(': stack.append(i)
        elif item == ')':
            if stack == []: return -1   #  more ')' than '(' in s
            stack.pop()
            n += 1
    if len(stack) > 0: return -1        #  more '(' than ')' in s
    return n

def check_with_benchmark(a,b,k):
    if len(a) != len(b): return "---{}-best instead of {}-best---".format(len(a),len(b))
    for i in range(len(a)):
        if a[i][0] != b[i][0]: return "---wrong # of pairs for {}th best---".format(i)
    dup, wrong = check_kbest(a, k)
    if not dup: return "---contain duplicate---"
    if wrong: return "---n and structure not match---"
    return True


if __name__ == "__main__":
    import time
    import sys


    ls = [  #"",
            #"A",
            "ACAGU",
            "UUCAGGA",
            "CAUCGGGGUCUG",     # total 1223
            #"UUGGACUUGAGAAAAG",
            #"CAUCGGGGUCUGAGAUGGCCAUGAAGGGCACGUACUGUUU",
            #"GCUGGCGGGCCCCUUCGCAUGGUUCGGCGGUGAAUCUGGUCAGGUCGGGAACGAAGCAGCCAUAGUCGUUCAGAACCAGUGCCGGAGUAAGGCUCGCCUACCGGUAUCCCU",
            #"GAAUGGCUCGGAUUUGAUGGGCCAUUCAACUUAUAACAGGCUCCGAAGUGACCUGUAACAGUGCCAAAAUGCGGGAAUUAGCCACCUUGGUGGUGAAACCCGCAGCUGAUCACCGCGUCAGUUCAACGACUAGAUGGUACUGGCUGGUUCGUUCCAGUUAAGAUAUAGUCUCUCACCGGGGGUAAAUCCCAGUGCUUCACGGCAUUAAAU"
            ]
    print("check with benchmark: on")
    for s in ls:
        print("\n{}\nseq: {}\nlen: {}, total: {}".format('-'*40,s, len(s),total(s))) 
        for k in [10,23,1223]:#(10,40,100,500,1000):

            t0 = time.time() 
            bench = rna_liang.kbest(s,k)
            t1 = time.time() - t0
            #print("time of {0}-best_liang:  {1:.3f}".format(k,time.time()-t0))

            t0 = time.time() 
            res = kbest_unlazy_bug(s,k)
            #print("{}-best_alg1.5:\n{}".format(k,kbest1(s,k)))
            print("\n{0}-best_unlazy_bug: {2},    time:{1:.3f}".format(k,time.time()-t0,len(res)))
            check = check_with_benchmark(res,bench,k)
            if check != True: print(check)


            t0 = time.time() 
            res = kbest_alg2_heapk(s,k)
            #print("{}-best_alg2_heapk:\n{}".format(k,len(res)))
            print("{0}-best_alg2_heapk: {2}, time:{1:.3f}".format(k,time.time()-t0,len(res)))
            check = check_with_benchmark(res,bench,k)
            if check != True: print(check)

            t0 = time.time() 
            res = kbest_alg2_heapn(s,k)
            #print("{}-best_alg2_heapn:\n{}".format(k,len(res)))
            print("{0}-best_alg2_heapn: {2}, time:{1:.3f}".format(k,time.time()-t0,len(res)))
            check = check_with_benchmark(res,bench,k)
            if check != True: print(check)

            t0 = time.time() 
            res = kbest_lazy_bug(s,k)
            print("{0}-best_lazy_bug: {2},     time:{1:.3f}".format(k,time.time()-t0,len(res)))
            check = check_with_benchmark(res,bench,k)
            if check != True: print(check)

            t0 = time.time() 
            res = kbest_lazy(s,k)
            #print("{}-best_lazy:\n{}".format(k,kbest(s,k)))
            print("{0}-best_lazy:  {2},     time:{1:.3f}".format(k,time.time()-t0,len(res)))
            check = check_with_benchmark(res,bench,k)
            if check != True: print(check)

            print("{0}-best_liang: {2},     time:{1:.3f}".format(k,t1,len(bench)))

 

    '''
    s = ""
    print(best(s))  #(0, '')
    s = "A"
    print(best(s))  #(0, '.')
    s = "ACAGU"
    print(best(s))  #(2, '((.))')
    s = "UUCAGGA"
    print(best(s))  #(3, '(((.)))')
    s = "GUUAGAGUCU"
    print(best(s))  #(4, '(.()((.)))')
    s = "GCACG"
    print(best(s))  #(2, '().()')
    s = "AUAACCUUAUAGGGCUCUG"
    print(best(s))  #(8, '.(((..)()()((()))))')
    s = "UUGGACUUGAGAAAAG"
    print(best(s))  #(5, '((...((()))...))')
    s = "UCAAUGGGUAGUAAAU"
    print(best(s))  #(6, '(((.)))((..(.)))')
    s = "UUUGGCACUUUCAGA"
    print(best(s))  #(6, '(((((.(..))))))')
    s = "ACACACCUUGUCCGUGAA"
    print(best(s))  #(6, '.((.(..)))(.()(.))')   
    s = "GAUGCCGUGUAGUCCAAAGACUUCACCGUUGG"
    print(best(s))  #(14, '.()()(()(()())(((.((.)(.))()))))')
    s = "CGCGAAUAAAAAGGCACUGUU"
    print(best(s))  #(8, '()()((((....(().)))))')
    s = "ACGGCCAGUAAAGGUCAUAUACGCGGAAUGACAGGUCUAUCUAC"
    print(best(s))  #(19, '.()(((.)(..))(((.()()(())))(((.)((())))))())')
    s = "UGGGUGAGUCGCACACUCUGCGUACUCUUUCCGUAAUU"
    print(best(s))  #(15, '.((()((((.()).(.)))(()())).((...()))))')
    s = "AUACGUCGGGGACAAGAAUUACGG"
    print(best(s))  #(8, '.(.(((()((..(..)..))))))')
    s = "AGGCAUCAAACCCUGCAUGGGAGCACCGCCACUGGCGAUUUUGGUA"
    print(best(s))  #(20, '.(()())...((((()()))((()(.()(((.)))()())))))()')
    s = "CGAGGUGGCACUGACCAAACACCACCGAAAC"
    print(best(s))  #(9, '.(.((((().)((.)..))).)...()...)')
    s = "CGCCGUCCGGGCGCGCCUUUUACGUAGAUUU"
    print(best(s))  #(12, '.(..(...((((())))(((.(())))))))')
    s = "CAUCGGGGUCUGAGAUGGCCAUGAAGGGCACGUACUGUUU"
    print(best(s))  #(18, '(()())(((((.)))()(((())(.(.().()()))))))')
    s = "AACCGCUGUGUCAAGCCCAUCCUGCCUUGUU"
    print(best(s))  #(11, '(((.(..(.((.)((...().))()))))))')
    
    s = "ACAGU"
    t = total(s)
    print("seq: {}\nbest: {}, total {}".format(s,best(s),t))   # ((.))'), 6
    m = 10
    print("{} best: {}\n".format(m,kbest(s,m)))

    s = "GUUAGAGUCU"#"ACAGU"
    t = total(s)
    print("seq: {}\nbest: {}, total {}".format(s,best(s),t))   # ((.))'), 6
    m = 10
    print("{} best: {}".format(m,kbest(s,m)))
    '''


    '''
    #s = "ACAGU"
    #s = "UUGGACUUGAGAAAAG"
    #s = "AGGCAUCAAACCCUGCAUGGGAGCG"
    #s = "CAUCGGGGUCUGAGAUGGCCAUGAAGGGCACGUACUGUUU"
    #s = "GCUGGCGGGCCCCUUCGCAUGGUUCGGCGGUGAAUCUGGUCAGGUCGGGAACGAAGCAGCCAUAGUCGUUCAGAACCAGUGCCGGAGUAAGGCUCGCCUACCGGUAUCCCU"
    #s = "GAAUGGCUCGGAUUUGAUGGGCCAUUCAACUUAUAACAGGCUCCGAAGUGACCUGUAACAGUGCCAAAAUGCGGGAAUUAGCCACCUUGGUGGUGAAACCCGCAGCUGAUCACCGCGUCAGUUCAACGACUAGAUGGUACUGGCUGGUUCGUUCCAGUUAAGAUAUAGUCUCUCACCGGGGGUAAAUCCCAGUGCUUCACGGCAUUAAAU"

    m = 50
    if len(sys.argv) > 1:
        m = int(sys.argv[1])

    print("seq: {}, len:{}\nbest: {}, total {}".format(s,len(s),best(s),total(s))) 
    t0 = time.time() 
    kbest(s,m)
    #print("{}-best:\n{}".format(m,kbest(s,m)))
    print("time of {}-best: {}".format(m,time.time()-t0))

    t0 = time.time() 
    kbest1(s,m)
    #print("{}-best1:\n{}".format(m,kbest1(s,m)))
    print("time of {}-best1: {}".format(m,time.time()-t0))

    t0 = time.time() 
    rna_liang.kbest(s,m)
    print("time of {}-best_liang: {}".format(m,time.time()-t0))
    '''



'''
## alg3: kbest(s,k)
## _wrong_: this version always add one TheNext, which will miss some candidates(i.e, [a,b] replaced by [a,b+1], the next optimal from [a,b+1] can only be [a+1,b+1]/[a,b+2], so [a+1,b] is omitted) 
## lazy generating
## O(n^3 + nklogn) time, O(n^2(n+k)) space
def kbest_lazy_bug(s, k):
    def solution(i, j, a):
        if i >= j: return ""
        mid = opt[i,j][a][1]
        if mid > i+1:       # case 2+3 
            return "("+solution(i+1,mid-1,opt[i,j][a][2])+")" + solution(mid,j,opt[i,j][a][3])
        if mid == i+1:      # case 1
            return "." + solution(mid, j, opt[i,j][a][3])
        return "."*(j-i)    # mid < 0

    def _next(i, j, kth):
        if branch[i,j] == [] or opt[i,j][-1][0] == 0: return None
        if kth < len(opt[i,j]): return opt[i,j][kth]
        n, mid, a, b = branch[i,j][0]
        TheNext = None
        if mid == i+1:      # case 1
            right = _next(mid,j,b+1)
            TheNext = (0, -1, 0, 0) if right is None else (right[0], mid, 0, b+1)   # __important__, to generate an empty one, not None
        elif mid > i+1:     # case 2+3
            left  = _next(i+1, mid-1, a+1)
            right = _next(mid, j,     b+1)
            if left is None and right is None: TheNext = (0, -1, 0, 0)              # __important__, to generate an empty one, not None
            elif left == None:
                TheNext = (opt[i+1,mid-1][a][0]+right[0]-1, mid, a, b+1)
            elif right == None:
                TheNext = (left[0]+opt[mid,j][b][0]-1, mid, a+1, b)
            else:
                if opt[i+1,mid-1][a][0]+right[0] < left[0]+opt[mid,j][b][0]:
                    TheNext = (opt[i+1,mid-1][a][0]+right[0]-1, mid, a, b+1)
                else: TheNext = (left[0]+opt[mid,j][b][0]-1, mid, a+1, b)

        if TheNext is None:         # the next of empty should be None, then this branch should be removed
            heappop(branch[i,j])
        else: 
            heapreplace(branch[i,j],TheNext)    # even next is empty, current branch should be replaced with a next one

        if branch[i,j] ==[]: return None
        opt[i,j].append(branch[i,j][0])
        return branch[i,j][0]

    l, res = len(s), []
    kth, a, b = 0, 0, 0
    opt = defaultdict(lambda:[(0,-2,0,0)])      # list of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], reversed list, sizeof m
    branch = defaultdict(lambda:[])             # heap of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], max-heap, sizeof j-i, it is the (mid-i)th branch
                                                # every time we want to extend the next largest one from opt[i+1,mid-1] and opt[mid,j]
    if s == '': return [(0, "")]
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d 
            if opt[i+1,j][kth][1] >= 0:
                opt[i,j][kth] = (opt[i+1,j][kth][0],i+1,a,b)    # case 1: .******* mid=i+1
                branch[i,j].append(opt[i,j][kth])               # init branch 0 for [i,j]
            for mid in range(i+2,j+1): 
                if s[i]+s[mid-1] in p:                            # case 2+3: (******) mid=j, or (***)*** mid=i+2..j-1
                    tmp_n = opt[i+1,mid-1][kth][0]+opt[mid,j][kth][0]-1
                    branch[i,j].append((tmp_n, mid, a, b))        # init the rest branches for [i,j]
                    if tmp_n < opt[i,j][kth][0]:
                        opt[i,j][kth] = branch[i,j][-1]
            heapify(branch[i,j])
    # by now, we solved 1-best, stored in opt[0,l][0], solution(0,l,0)
    res.append((-opt[0,l][kth][0],solution(0,l,kth)))
    for kth in range(1,k):
        TheNext = _next(0,l,kth)    
        if TheNext is None: break
        res.append((-opt[0,l][kth][0],solution(0,l,kth)))
    return res



## alg1.5: kbest1(s,k)
## unlazy kbest, Serial_push -> maitain_heap_size -> list -> opt[i,j]
## O(klogk*n^3) time, O(k*n^2) space
## n^2*(heapify O(k) + put:O(klogk) + 3rd_loop O(n*2k*logk) + sort O(klogk) )
def kbest_unlazy_bug(s, k):
    def solution(i,j,a):
        if i >= j: return ""
        mid = opt[i,j][a][1]
        if mid == -1:
            return "("+solution(i+1,j-1,opt[i,j][a][2])+")"
        elif mid > 0:
            return solution(i, mid, opt[i,j][a][2]) + solution(mid, j, opt[i,j][a][3])
        return "."*(j-i)

    def put(i,j,n,mid,a,b,k):
        #n = opt[i,mid][a][0] + opt[mid,j][b][0]
        if n == 0 : return 0
        if (n,mid,a,b) in opt[i,j]: return 1
        if len(opt[i,j]) < k:   # heap opt[i,j] has elements less than k, push
            heappush(opt[i,j],(n,mid,a,b))
            return 1
        elif n > opt[i,j][0][0]:# heap opt[i,j] has m elements and the new one > heapmin, replace
            heapreplace(opt[i,j],(n,mid,a,b))
            return 1
        else: return 0

    l, res = len(s), []
    opt = defaultdict(lambda:[(0,-2,0,0)]) #list of tuple (n_pair, mid, l_idx, r_idx)
    if s == '': return [(0, "")]
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d            
            
            opt[i,j] = [(n,i+1,0,a) for a, (n,_,_,_) in enumerate(opt[i+1,j])]  # case 1: .*******
            heapify(opt[i,j])
            if s[i]+s[j-1] in p:
                for a, (n,_,_,_) in enumerate(opt[i+1,j-1]):    # case 2: (******)
                    put(i,j,n+1,-1,a,-1,k)

            for mid in range(i+2,j):  #mid = i+2..j-1
                if s[i]+s[mid-1] in p:  # case 3: (***)***
                    a, b = 0, 0
                    while a < len(opt[i,mid]) and opt[i,mid][a][1] != -1: a += 1 # find a candidate a, st opt[i,j][a] has an outter pair
                    while a < len(opt[i,mid]) and b < len(opt[mid,j]):
                        if put(i,j,opt[i,mid][a][0]+opt[mid,j][b][0],mid,a,b,k) == 0: break 

                        a1, b1 = a+1, b+1
                        while a1 < len(opt[i,mid]) and opt[i,mid][a1][1] != -1: a1 += 1
                        if a1 < len(opt[i,mid]) and b1 < len(opt[mid,j]):
                            if opt[i,mid][a1][0]+opt[mid,j][b][0] >= opt[i,mid][a][0]+opt[mid,j][b1][0]:
                                a = a1
                            else: b = b1
                        elif a1 < len(opt[i,mid]):
                            a = a1
                        elif b1 < len(opt[mid,j]):
                            b = b1
                        else: break
            opt[i,j] = nlargest(k,opt[i,j])
            #opt[i,j].sort(reverse=True)

    #pdb.set_trace()
    for a, kth in enumerate(opt[0,l]):
        res.append((kth[0],solution(0,l,a)))
            
    return res 
'''