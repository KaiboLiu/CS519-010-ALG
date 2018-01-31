import heapq

def ksmallest(k,a):
    h = [ -i for i in a[:k] ]   
    l = len(a)
    heapq.heapify(h)
    for i in range(k,l):
        if -a[i] <= h[0]:
            continue
        heapq.heapreplace(h,-a[i])
    return [-i for i in heapq.nlargest(k,h)]
    # O(k+(n-k)logk*2+klogk)=O(2nlogk-klogk+k)

if __name__ == "__main__":
    print(ksmallest(4, [10, 2, 9, 3, 7, 8, 11, 5, 7]))
    #[2, 3, 5, 7]
    print(ksmallest(3, range(1000000, 0, -1)))
    #[1, 2, 3]
    
