def mergesort(a):
	if len(a) <= 1: return a
	mid = int(len(a) / 2)
	return merge(mergesort(a[:mid]),mergesort(a[mid:]))


def merge(a,b):
	i, j, c = 0, 0, []
	while i < len(a) and j < len(b):
		if a[i] <= b[j]:
			c.append(a[i])
			i += 1
		else: 
			c.append(b[j])
			j += 1
	c[len(c):len(c)] = a[i:] if i < len(a) else b[j:]
	return c


if __name__ == "__main__":
	print(mergesort([4, 2, 5, 1, 6, 3]))