from collections import defaultdict
import pdb

p = {'AU','UA','CG','GC','UG','GU'}

def best(s):
    opt, strc = defaultdict(int), defaultdict(lambda:'.')
    l = len(s)

    if l <= 1: return 0
    for d in range(2,l+1):  # d=delta range, length of range[i,j]:s[i]..s[j-1]
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
    '''        
    def solution(a,b,n):
        if a+2 > b: return 
        for i in range(a,b-1):
            if i in pair and pair[i] < b and opt[i,pair[i]+1]+opt[pair[i]+1,b] == n:
                #print(i,pair[i],b,opt[i,pair[i]],opt[pair[i]+1,b])
                #print(i,pair[i])
                strc[i], strc[pair[i]] = '(', ')' 
                #solution(a,i-1)
                solution(i+1,pair[i],opt[i,pair[i]+1]-1)
                solution(pair[i]+1,b,opt[pair[i]+1,b])
                return
    
    solution(0,l,opt[0,l])
    '''
    #pdb.set_trace()
    #print(pair)
    
    return opt[0,l], strc[0,l]




if __name__ == "__main__":

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
   
    '''
