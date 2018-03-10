'''
Developer: Kaibo(lrushx)
Email: liukaib@oregonstate.edu
Process Time: Feb 28, 2018
'''

from collections import defaultdict
from heapq import heapify, heapreplace, heappush, heappop
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
## 1. O(n^3k+n^2klogk)  push all into heap
## 2. O(n^3 +n^2klogk)  mantain the size of heap    - kbest1(s,m)
## 3. O(n^3 +nklogk)    lazy heap                   - kbest(s,m)

## lazy version
## O(n^3 +nklogk)
def kbest(s, m):
    def solution(i, j, a):
        if i >= j: return ""
        mid = opt[i,j][a][1]
        if mid > i+1:       # case 2+3 
            return "("+solution(i+1,mid-1,opt[i,j][a][2])+")" + solution(mid,j,opt[i,j][a][3])
        if mid == i+1:      # case 1
            return "." + solution(mid, j, opt[i,j][a][3])
        return "."*(j-i)    # mid < 0

    def _next(i, j, mth):
        if branch[i,j] == [] or opt[i,j][-1][0] == 0: return None
        if mth < len(opt[i,j]): return opt[i,j][mth]
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
    mth, a, b = 0, 0, 0
    opt = defaultdict(lambda:[(0,-2,0,0)])      # list of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], reversed list, sizeof m
    branch = defaultdict(lambda:[])             # heap of tuple (-n_pair, mid, l_idx, r_idx) for [i,j], max-heap, sizeof j-i, it is the (mid-i)th branch
                                                # every time we want to extend the next largest one from opt[i+1,mid-1] and opt[mid,j]
    if s == '': return 0, ""
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d 
            if opt[i+1,j][mth][1] >= 0:
                opt[i,j][mth] = (opt[i+1,j][mth][0],i+1,a,b)    # case 1: .******* k=i+1
                branch[i,j].append(opt[i,j][mth])               # init branch 0 for [i,j]
            for k in range(i+2,j+1): 
                if s[i]+s[k-1] in p:                            # case 2+3: (******) k=j, or (***)*** k=i+2..j-1
                    tmp_n = opt[i+1,k-1][mth][0]+opt[k,j][mth][0]-1
                    branch[i,j].append((tmp_n, k, a, b))        # init the rest branches for [i,j]
                    if tmp_n < opt[i,j][mth][0]:
                        opt[i,j][mth] = branch[i,j][-1]
            heapify(branch[i,j])
    # by now, solved 1-best, stored in opt[0,l][0], solution(0,l,0)
    res.append((-opt[0,l][mth][0],solution(0,l,mth)))
    for mth in range(1,m):
        TheNext = _next(0,l,mth)    
        if TheNext is None: break
        res.append((-opt[0,l][mth][0],solution(0,l,mth)))
    return res


## O(klogk*n^3) time + O(k*n^2) space
## n^2*(heapify O(k) + put:O(klogk) + 3rd_loop O(n*2k*logk) + sort O(klogk) )
def kbest1(s, m):
    def solution(i,j,a):
        if i >= j: return ""
        mid = opt[i,j][a][1]
        if mid == -1:
            return "("+solution(i+1,j-1,opt[i,j][a][2])+")"
        elif mid > 0:
            return solution(i, mid, opt[i,j][a][2]) + solution(mid, j, opt[i,j][a][3])
        return "."*(j-i)

    def put(i,j,n,mid,a,b,m):
        #n = opt[i,mid][a][0] + opt[mid,j][b][0]
        if n == 0 : return 0
        if (n,mid,a,b) in opt[i,j]: return 1
        if len(opt[i,j]) < m:   # heap opt[i,j] has elements less than m, push
            heappush(opt[i,j],(n,mid,a,b))
            return 1
        elif n > opt[i,j][0][0]:# heap opt[i,j] has m elements and the new one > heapmin, replace
            heapreplace(opt[i,j],(n,mid,a,b))
            return 1
        else: return 0

    l, res = len(s), []
    opt = defaultdict(lambda:[(0,-2,0,0)]) #list of tuple (n_pair, mid, l_idx, r_idx)
    if s == '': return []
    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d            
            
            opt[i,j] = [(n,i+1,0,a) for a, (n,_,_,_) in enumerate(opt[i+1,j])]  # case 1: .*******
            heapify(opt[i,j])
            if s[i]+s[j-1] in p:
                for a, (n,_,_,_) in enumerate(opt[i+1,j-1]):    # case 2: (******)
                    put(i,j,n+1,-1,a,-1,m)

            for k in range(i+2,j):  #k = i+2..j-1
                if s[i]+s[k-1] in p:  # case 3: (***)***
                    a, b = 0, 0
                    while a < len(opt[i,k]) and opt[i,k][a][1] != -1: a += 1 # find a candidate a, st opt[i,j][a] has an outter pair
                    while a < len(opt[i,k]) and b < len(opt[k,j]):

                        if put(i,j,opt[i,k][a][0]+opt[k,j][b][0],k,a,b,m) == 0: break 

                        a1, b1 = a+1, b+1
                        while a1 < len(opt[i,k]) and opt[i,k][a1][1] != -1: a1 += 1
                        if a1 < len(opt[i,k]) and b1 < len(opt[k,j]):
                            if opt[i,k][a1][0]+opt[k,j][b][0] >= opt[i,k][a][0]+opt[k,j][b1][0]:
                                a = a1
                            else: b = b1
                        elif a1 < len(opt[i,k]):
                            a = a1
                        elif b1 < len(opt[k,j]):
                            b = b1
                        else: break
            #opt[i,j] = nlargest(m,opt[i,j])
            opt[i,j].sort(reverse=True)

    #pdb.set_trace()
    for a, mth in enumerate(opt[0,l]):
        res.append((mth[0],solution(0,l,a)))
            
    return res 


################### part0 customized check ########################################################

def check_kbest(res, m):
    check, wrong = set(), 0
    for n,s in res: 
        check.add(s)
        if cntPairs(s) != n: wrong += 1
    return len(check), wrong

    
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

if __name__ == "__main__":
    import time
    import sys
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


    ls = [  "UUGGACUUGAGAAAAG",
            "CAUCGGGGUCUGAGAUGGCCAUGAAGGGCACGUACUGUUU",
            "GCUGGCGGGCCCCUUCGCAUGGUUCGGCGGUGAAUCUGGUCAGGUCGGGAACGAAGCAGCCAUAGUCGUUCAGAACCAGUGCCGGAGUAAGGCUCGCCUACCGGUAUCCCU",
            "GAAUGGCUCGGAUUUGAUGGGCCAUUCAACUUAUAACAGGCUCCGAAGUGACCUGUAACAGUGCCAAAAUGCGGGAAUUAGCCACCUUGGUGGUGAAACCCGCAGCUGAUCACCGCGUCAGUUCAACGACUAGAUGGUACUGGCUGGUUCGUUCCAGUUAAGAUAUAGUCUCUCACCGGGGGUAAAUCCCAGUGCUUCACGGCAUUAAAU"
            ]
    for s in ls:
        print("seq: {}\nlen: {}".format(s, len(s))) 
        for m in (10,50):
            t0 = time.time() 
            kbest1(s,m)#print("{}-best_unlazy:\n{}".format(m,kbest1(s,m)))
            print("time of {}-best_unlazy: {}".format(m,time.time()-t0))
            #print("time of {0}-best_unlazy: {1:.3f}".format(m,time.time()-t0))

            t0 = time.time() 
            kbest(s,m)
            #print("{}-best_lazy:\n{}".format(m,kbest(s,m)))
            print("time of {}-best_lazy:   {}".format(m,time.time()-t0))

            t0 = time.time() 
            rna_liang.kbest(s,m)
            #print("{}-best_liang:\n{}".format(m,rna_liang.kbest(s,m)))
            print("time of {}-best_liang:  {}".format(m,time.time()-t0))
        print(" ")


    #distinct, wrong = check_kbest(res,m)
    #print("check distinct: {}, wrong: {}".format(distinct, wrong))

    #for m in range(t):
    #    print("{} best: {}".format(m+1,kbest(s,m+1)))
    
    #print(kbest("ACAGU", 5)) # [(2, '((.))'), (1, '(...)'), (1, '.(.).'), (1, '...()'), (1, '..(.)'), (0, '.....')]

    '''
    import time
    from random import randint,seed
    seed(10)   #random.seed
    cases = 5
    node = ['A','U','C','G']
    for i in range(cases):
        l = randint(10,200)
        s = [node[randint(0,3)] for _ in range(l)]
        s = ''.join(s)
        time0 = time.time()
        n1, res1 = best(s)
        time1 = time.time()
        n2, res2 = best1(s)
        time2 = time.time()
         
        if n1 != n2: print('not same value: {} {}'.format(n1, n2))
        else: print('same value: {}'.format(n1))
        print('1 has {} pairs'.format(cntPairs(res1)))
        print('2 has {} pairs'.format(cntPairs(res2)))
        
        print('length: {}  pairs: {}\ntime1:{}\ntime2:{}'.format(l,n1,time1-time0, time2-time1))
    '''
