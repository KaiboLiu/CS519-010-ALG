from collections import defaultdict
import pdb

p = {'AU','UA','CG','GC','UG','GU'}



## trace back with recurrsion + middle point
def best(s):
    def solution(a,b):
        if a >= b: return ""
        if a == b-1: return "."
        if mid[a,b] == -1:
            return "("+solution(a+1,b-1)+")"
        elif mid[a,b] > 0:
            return solution(a, mid[a,b]) + solution(mid[a,b], b)
        return ""

    opt, mid = defaultdict(int), defaultdict(int)#(lambda:-1)
    if s == '': return 0,''
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
def best1(s):
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


def total(s):
# 2 cases: .*******, (***)*** or (******)
    opt, l = defaultdict(int), len(s)
    for i in range(l+1):
        opt[i,i], opt[i,i+1] = 1, 1 # single and empty

    for d in range(2,l+1):  # d=delta range, length of range[i,j], s[i]..s[j-1]
        for i in range(l-d+1):    # j=i+d
            j = i+d 
            opt[i,j] += opt[i+1,j]  # case 1

            for k in range(i+2,j+1):  #k = i+2..j, to pair s[i] with s[k-1]
                if s[i]+s[k-1] in p:
                    opt[i,j] += opt[i+1,k-1] * opt[k,j] # case 2
    return opt[0,l]

def kbest(s, m):
    

def cntPairs(s):
    stack, n = [],0
    for i, item in enumerate(s):
        if item == '(':
            stack.append(i)
        elif item == ')':
            j = stack.pop()
            n += 1
    return n

if __name__ == "__main__":

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
    '''

    
    print(total("ACAGU"))
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