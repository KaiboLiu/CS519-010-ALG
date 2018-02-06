import heapq
# this version uses index of a list, which will be slower
'''
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
'''

def ksmallest(k,a):
    h = []
    l, i = len(a), 0

    for x in a:
        if i < l: 
            heapq.heappush(h,-x)
            i = i + 1
        else: 
            if -x <= h[0]: continue
            heapq.heapreplace(h,-x)
    return [-i for i in heapq.nlargest(k,h)]


if __name__ == "__main__":
    print(ksmallest(4, [10, 2, 9, 3, 7, 8, 11, 5, 7]))
    #[2, 3, 5, 7]
    print(ksmallest(3, range(1000000, 0, -1)))
    #[1, 2, 3]
    
