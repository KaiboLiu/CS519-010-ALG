from time import time



if __name__ == '__main__':
    print('test for list addition a + b:')
    n = 10000000
    print('gengerating size for a, b:',n)

    start_time = time()
    a = list(range(n))
    b = list(range(n))
    print('time: %s, generating lists.' % (time()-start_time))
    
    start_time = time()    
    for x in b: a.append(x)
    print('time: %s, append in for loop, (for x in b: a.append(x)).' % (time()-start_time))

    a = list(range(n))
    start_time = time()
    c = a + b
    print('time: %s, with list add, (a + b).' % (time()-start_time))

    start_time = time()
    a.extend(b)
    print('time: %s, with extend, (a.extend(b)).' % (time()-start_time))

    a = list(range(n))
    start_time = time()
    a[len(a):len(a)] = b
    print('time: %s, slice append, (a[len(a):len(a)] = b).' % (time()-start_time))

    a = list(range(n))
    start_time = time()
    a[n:n] = b
    print('time: %s, slice append, (a[n:n] = b).' % (time()-start_time))