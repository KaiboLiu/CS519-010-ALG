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
