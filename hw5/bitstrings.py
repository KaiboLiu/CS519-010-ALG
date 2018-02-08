## no two consecutive 0s. for s[1..n], either add 1 to s[1..n-1] or add 10. to s[1..n-2]
## f(n)=f(n-1)+f(n-2), f(-1)=f(0)=1, f(1)=2
def num_no(n):
    a, b = 1, 1
    for i in range(n): 
        a, b = b, a+b

    return b


## two consecutive 0s. for s[1..n], either add 0 to s[1..n-1] or add 00. to s[1..n-2]
## f(n)=3*2^(n-3)+2*f(n-2)+f(n-3), f(0)=f(1)=0, f(2)=1
def num_yes2(n):
    #return (1<<n) - num_no(n)
    f = {0:0, 1:0, 2:1, 3:0}
    if n < 3: return f[n]
    ex = 3
    for i in range(3,n+1):
        f[3] = ex + 2*f[1] + f[0]
        f[0], f[1], f[2] = f[1], f[2], f[3]#
        ex = ex << 1

    return f[3]

## or, num_yes(n) = (1<<n)-num_no(n),
## because num_yes(n) + num_no(n) == 2^n
def num_yes(n):
    return (1<<n)-num_no(n)

if __name__ == "__main__":
    print(num_no(3))
    ## 5
    print(num_yes(3))
    ## 3
#    for i in range(10):
#        print("%d: %d <--> %d"%(i,num_no(i),num_yes(i)))