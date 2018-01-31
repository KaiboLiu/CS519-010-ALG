import heapq

def kmergesort(a,k):
    l = len(a)
    if l <= 1: return a
    step = (l-1)//k + 1
    lists = [kmergesort(a[i:i+step],k) for i in range(0,l,step)]
    print(lists)
    return list(heapq.merge(*lists))


if __name__ == "__main__":
    print(kmergesort([4,1,5,2,6,3,7,0], 3))
    #[0,1,2,3,4,5,6,7]