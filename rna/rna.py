def best(s):
    l = len(s)


if __name__ == "__main__":
    
    s = "ACAGU"
    print(s)
    print(best(s))
    # (2, '((.))')
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
   

