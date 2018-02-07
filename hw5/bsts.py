## Number of n-node BSTs (isomorphic are counted as duplicate)
## Let's consider n-node, except the root, it can be divided to left(i) and right(n-1-i), just multiply them, and visit all the possible i (1=0..n-1)

## This is a DP method with O(n^2)
## I didn't write the mathamatical way of directly calculating C(2n,n)/(n+1), which is O(n).
def bsts(n):
    if n < 2: return 1
    f = [0] * (n+1)
    f[0] = f[1] = 1
    for m in range(2,n+1):
        for i in range((m-2)//2 + 1):
            f[m] = f[m] + 2*f[i]*f[m-i-1]
        if m & 1: f[m] = f[m] + f[m//2]*f[m//2]
    return f[n]


if __name__ == "__main__":
    print(bsts(2))
    ## 2
    print(bsts(3))
    ## 5
    print(bsts(5))
    ## 42