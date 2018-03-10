'''
Developer: Kaibo(lrushx)
Email: liukaib@oregonstate.edu
Process Time: Mar 1, 2018
'''

from collections import defaultdict
import time

class keyPQ():  # decrease-key priority queue
    def __init__(self, h=[]):
        self.heap = h           # list of [weight, V] in heap
        self.len  = len(h)
        self.popped = set()
        self.idx  = defaultdict(lambda:-1)
        for i,(_,v) in enumerate(h): self.idx[v] = i
        self.heapify()

    def heapify(self):
        i0 = self.len >> 1
        for i in range(i0,-1,-1): 
            self.sink(i)

    def push(self, item):
        self.heap.append(item)
        self.idx[item[1]] = self.len
        self.rise(self.len)
        self.len += 1

    def pop(self):
        if self.len == 0: return None
        self.len -= 1
        self.switch(0,self.len)
        top = self.heap.pop()
        self.popped.add(top[1])
        self.sink(0)
        return top

    def sink(self, i):
        l, r = i+i+1, i+i+2
        if l >= self.len: return
        if r >= self.len and self.heap[i][0] > self.heap[l][0]:
            self.switch(i, l)
            self.sink(l)
        if r < self.len:
            minChild = l if self.heap[l][0] < self.heap[r][0] else r
            if self.heap[i][0] > self.heap[minChild][0]:
                self.switch(i, minChild)
                self.sink(minChild)

    def rise(self, i):
        if i == 0: return 
        parent = (i-1)>>1
        if self.heap[i][0] < self.heap[parent][0]:
            self.switch(i, parent)
            self.rise(parent)

    def switch(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.idx[self.heap[i][1]], self.idx[self.heap[j][1]] = i, j 

    def decreaseKey(self, i, w):
        self.heap[i][0] = w
        self.rise(i)


## O((V+E)logV)
def shortest(n, edges):

    def solution(v, back):
        if v == start: return [v]
        return solution(back[v],back)+[v]

    weight, edge = defaultdict(lambda: 1<<30), defaultdict(set)
    dist, back = defaultdict(lambda:-1), defaultdict(int)
    for (u,v,w) in edges:
        weight[u,v] = weight[v,u] = w #  = min(weight[u,v],w)
        edge[u].add(v)
        edge[v].add(u)  
    start, end = 0, n-1
    # init 1: put all the start's neighbors to the heap, and heapify, O(n1)
    h = []
    for v in edge[start]:
        h.append([weight[start, v], v])
        dist[v], back[v] = weight[start,v], start 
    q = keyPQ(h)
    # init 2: put start to the heap, O(1), but push its neighbors later one by one, O(n1logn1)
    #q = keyPQ([[0,start]])
    while q.len:
        w0, u = q.pop()
        if u == end: break
        for v in edge[u]:  
            if v in q.idx:          # v in the queue and not popped yet
                if v in q.popped: continue
                w, w1 = q.heap[q.idx[v]][0], weight[u,v]+w0   
                if w1 < w:
                    q.decreaseKey(q.idx[v],w1)
                    dist[v], back[v] = w1, u
            else:                   # the rest nodes linked to u, which are not in the queue,  q.idx[v] == -1   
                q.push([w0+weight[u,v], v])
                dist[v], back[v] = w0+weight[u,v], u
               
    if dist[end] == -1: return None
    return dist[end], solution(end,back)

if __name__ == "__main__":

    print(shortest(4, [(0,1,1), (0,2,5), (1,2,1), (2,3,2), (1,3,6)]))
    # (4, [0,1,2,3])
    print(shortest(5,[(0,2,24),(0,4,20),(3,0,3),(4,3,12)]))
    #(15, [0, 3, 4])
    '''
    q = keyPQ([[6,2],[5,3],[3,4],[20,5],[12,6],[2,7]])
    q.pop()
    q.push([0,0])
    print(q.heap)
    '''
    #pdb.set_trace()
    

    import sys
    #sys.path.append("/nfs/farm/classes/eecs/winter2018/cs519-010/include")
    def generate_seq(k,length,seed): import random; random.seed(seed); return [tuple(sorted(random.sample(range(k),2))+[random.randint(5,10)]) for _ in range(length)]
    #tuple1 = generate_seq(10,50,1)
    #print(tuple1)
    dense_tuples = generate_seq(1000, 50000, 1)
    tuples_1 = generate_seq(5000, 50000, 1)
    tuples_2 = generate_seq(5000, 50000, 4)
    V,E = 1000, 5000
    t1 = time.time()
    print(shortest(V, dense_tuples[:E]))
    print("V={}, E={}, total time {}".format(V, E,time.time()-t1))

    V,E = 1000, 10000
    t1 = time.time()
    print(shortest(V, dense_tuples[:E]))
    print("V={}, E={}, total time {}".format(V, E,time.time()-t1))

    V,E = 5000, 50000
    t1 = time.time()
    print(shortest(V, tuples_1))
    print("V={}, E={}, total time {}".format(V, E,time.time()-t1))

    V,E = 5000, 50000
    t1 = time.time()
    print(shortest(V, tuples_2))
    print("V={}, E={}, total time {}".format(V, E,time.time()-t1))
#    tuples_1 = generate_seq(5000, 50000, 1)
#    tuples_2 = generate_seq(5000, 50000, 4)
