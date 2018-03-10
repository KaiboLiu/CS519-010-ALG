__author__ = "liang huang" # version 2, semiring

from heapq import heapify, heappop, heappush
from collections import defaultdict
allowed = set(['AU','UA','CG','GC','GU','UG'])

def common(s, plus, times1, times2, plus_unit, times_unit):

    def update(i, j, value1, value2=None):
        if value2 is None:
            tot[i, j] = plus(tot[i, j], times1(value1))
        else:
            tot[i, j] = plus(tot[i, j], times2(value1, value2))

    n = len(s)
    tot = defaultdict(lambda: plus_unit)

    for i in range(n+1): # N.B.: n+1: tot[n, n] = 1
        tot[i, i+1] = times1(times_unit) # singleton '.'
        tot[i, i] = times_unit # empty '' 

    for span in range(2, n+1): # span length: 2..n
        for i in range(n-span+1): # left boundary: 0..(n-span)
            j = i+span # right boundary
            
            update(i, j, tot[i+1, j]) # case 1: i unpaired 

            for k in range(i+1, j+1): # case 2: i paird with some k-1
                if s[i]+s[k-1] in allowed: # i( ___ )k ____ j
                    update(i, j, tot[i+1, k-1], tot[k, j])
            
    return tot[0, n]

def total(s):
    return common(s, lambda x,y: x+y, lambda x: x, lambda x,y: x*y, 0, 1) # (+, *, 0, 1) semiring

def best(s):
    return common(s, 
                  lambda x,y: max(x,y), 
                  lambda x: (x[0], ".%s" % x[1]),
                  lambda x,y: (x[0]+y[0]+1, "(%s)%s" % (x[1], y[1])),
                  (float("-inf"), ''), 
                  (0, '')) # (max, +, -inf, 0) semiring

def kbest(s, k): # using the division in total (no need to check duplicate), not in best
    '''Huang and Chiang 2005 Algorithm 2'''

    left = lambda m: opt[i+1, m-1]  # i ( xxx ) m ___ j
    right = lambda m: opt[m, j]     # i ( ___ ) m xxx j
    single = lambda : opt[i+1, j]   # i . xxxxxxxxxxx j

    def tryadd(split, index1, index2, func=heappush): # i paired with split-1
        if index1 < len(left(split)) and index2 < len(right(split)) \
           and not (split, index1, index2) in used:
            used.add((split, index1, index2))
            func(heap, 
                 (-left(split)[index1]-right(split)[index2]-1, split, index1, index2)) # pair

    def tryadd1(index, func=heappush):
        if index < len(single()):
            func(heap, (-single()[index], index)) # min-heap, i unpaired

    def solution(i, j, index):
        if i == j: return "" # empty
        if i == j-1: return "." # singleton
        split, index1, index2 = back[i, j][index]
        if split is None:
            return ".%s" % solution(i+1, j, index1)
        return "(%s)%s" % (solution(i+1, split-1, index1),
                           solution(split, j, index2))
        
    n = len(s)
    opt = defaultdict(list) # list of values
    back  = defaultdict(list)
    for i in range(n+1):# N.B. opt[n,n]=0
        opt[i, i+1] = [0] # singleton
        opt[i, i] = [0] # empty

    for span in range(2, n+1): # span length: 2..n
        for i in range(n-span+1): # left boundary: 0..(n-span)
            j = i+span # right boundary

            heap, used = [], set()

            tryadd1(0, func=list.append) # i unpaired  # don't heappush
            for m in range(i+1, j+1): # i pair with some k
                if s[i]+s[m-1] in allowed: # i( ___ )k ___ j
                    tryadd(m, 0, 0, func=list.append) # dont' heappush

            heapify(heap)

            while heap != [] and len(opt[i, j]) < k:
                item = heappop(heap)
                if len(item) == 2: # i unpaired
                    value, index = item
                    opt[i,j].append(-value)
                    back[i,j].append((None, index, None))
                    tryadd1(index+1)
                else: # i paired, split
                    value, split, index1, index2 = item
                    opt[i,j].append(-value)
                    back[i,j].append((split, index1, index2))
                    tryadd(split, index1+1, index2)
                    tryadd(split, index1, index2+1)

    return [(opt[0,n][p], solution(0,n,p)) for p in range(min(k, len(opt[0,n])))]

if __name__ == "__main__":

    testcases = [
        "ACAGU",
        "UUCAGGA",
        "GUUAGAGUCU",
        "GCACG",
        "AUAACCUUAUAGGGCUCUG",
        "UUGGACUUGAGAAAAG",
        "UCAAUGGGUAGUAAAU",
        "UUUGGCACUUUCAGA",
        "ACACACCUUGUCCGUGAA",
        "GAUGCCGUGUAGUCCAAAGACUUCACCGUUGG",
        "CGCGAAUAAAAAGGCACUGUU",
        "ACGGCCAGUAAAGGUCAUAUACGCGGAAUGACAGGUCUAUCUAC",
        "UGGGUGAGUCGCACACUCUGCGUACUCUUUCCGUAAUU",
        "AUACGUCGGGGACAAGAAUUACGG",
        "AGGCAUCAAACCCUGCAUGGGAGCACCGCCACUGGCGAUUUUGGUA",
        "CGAGGUGGCACUGACCAAACACCACCGAAAC",
        "CGCCGUCCGGGCGCGCCUUUUACGUAGAUUU",
        "CAUCGGGGUCUGAGAUGGCCAUGAAGGGCACGUACUGUUU",
        "AACCGCUGUGUCAAGCCCAUCCUGCCUUGUU",
]

    # testcases = [
    #     "ACAGU",
    #     "AC",
    #     "GUAC",
    #     "GCACG",
    #     "CCGG",
    #     "CCCGGG"
    #     "UUCAGGA",
    #     "AUAACCUA",
    #     "UUGGACUUG",
    #     "UUUGGCACUA",
    #     "GAUGCCGUGUAGUCCAAAGACUUC",
    #     "AGGCAUCAAACCCUGCAUGGGAGCG",
    # ]

    testcases = [
        # "GACUGGAAGGUUGGCAGCUUCUGUAAUCACGCUUCUGUGAGGUCUGAUUGUGGGAUGGCCUGAGGCUGGGAAUCACUGUGUAGCGGACCAGCUCAUGUUGACGGAACGUCCGCACUAAGCUUGACAUCAAUAUGGGUGCCAUGGAGGAGUCCACGGCAUUCAGGUUGGCCAAGGAGGGACGAACCGGGCCAGGGGUGAAAACCAGCAGCCAAGAGUUCCCGUGUUAGGCAGUAGUGGGAUAGCGUACCGGAGUGAACUGCCGUUAUCAGCCCAACCAAUUAUGGUUGGACCACAAUCUUUU", 
         "GCUGGCGGGCCCCUUCGCAUGGUUCGGCGGUGAAUCUGGUCAGGUCGGGAACGAAGCAGCCAUAGUCGUUCAGAACCAGUGCCGGAGUAAGGCUCGCCUACCGGUAUCCCU"
    ]    

    for testcase in testcases:
        print(testcase)
        print(best(testcase))
        print(total(testcase))
        print(kbest(testcase, 10))
        print("------")
