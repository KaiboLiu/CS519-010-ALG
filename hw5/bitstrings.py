## no two consecutive 0s. for s[1..n], either add 1 to s[1..n-1] or add 10. to s[1..n-2]
def num_no(n):
    f = {0:1, 1:2, 2:0}
    if n < 2: return f[n]
    for i in range(2,n+1): 
        f[2] = f[0] + f[1]
        f[0], f[1] = f[1], f[2]

    return f[2]


## two consecutive 0s. for s[1..n], either add 1 to s[1..n-1] or add 10. to s[1..n-2]
def num_yes(n):
    return (1<<n) - num_no(n)


if __name__ == "__main__":
    print(num_no(3))
    ## 5
    print(num_yes(3))
    ## 3