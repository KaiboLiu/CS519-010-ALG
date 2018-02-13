def bsts(n):
    num = {0:1}
    for i in range(1, n+1):
        num[i] = sum(num[j] * num[i-j-1] for j in range(i))
    return num[n]

for i in range(10):
    print(i, bsts(i))
