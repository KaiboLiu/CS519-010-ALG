def num_no(n): # similar to O(1)-space Fibonacci
    a, b = 1, 1
    for i in range(n):
        a, b = b, a + b
    return b

num_yes = lambda n: 2**n - num_no(n)

print(num_no(3))
print(num_no(1))
print(num_no(0))
print(num_yes(3))
