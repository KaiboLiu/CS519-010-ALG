'''
Developer: Kaibo(lrushx)
Email: liukaib@oregonstate.edu
Process Time: Mar 1, 2018
'''

from collections import defaultdict
import time

'''
class keyPQ():  # decrease-key priority queue
    def __init__(self, h=[]):
        self.heap = h           # list of [weight, V] in heap
        self.len  = len(h)
        self.popped = set()
        self.idx  = defaultdict(lambda:-1)
        for i,(_,v,_) in enumerate(h): self.idx[v] = i
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

    def decreaseKey(self, i, w, prev):
        self.heap[i][0], self.heap[i][2] = w, prev
        self.rise(i)


## O((V+E)logV), decrease-key heap
## 0.769 s on flip test
def shortest1(n, edges):
    def solution(v, back):
        if v == start: return [v]
        return solution(back[v],back)+[v]

    edge = defaultdict(set)
    back = {}
    for (u,v,w) in edges:
        #weight[u,v] = weight[v,u] = min(weight[u,v],w)
        edge[u].add((v,w))
        edge[v].add((u,w))  
    start, end = 0, n-1
    # init 1: put all the start's neighbors to the heap, and heapify, O(n1)
    global npop, npush
    npop, npush = 0, 1
    h = [[0, start, -1]]    #[dist, node, prev]
    for v,w in edge[start]:
        h.append([w, v, start])
        npush += 1
    q = keyPQ(h)
    while q.len:
        w0, u, prev = q.pop()
        npop += 1
        back[u] = prev
        if u == end: return w0, solution(end,back)
        for v,w in edge[u]:  
            w1 = w0 + w
            if v in q.idx:          # v in the queue and not popped yet
                if v in q.popped: continue
                if w1 < q.heap[q.idx[v]][0]:
                    q.decreaseKey(q.idx[v],w1,u)
                    npush += 1
            else:                   # the rest nodes linked to u, which are not in the queue,  q.idx[v] == -1   
                q.push([w1, v, u])
                npush += 1
    return None



## O((V+E)logV), decrease-key heap-dict from https://gist.github.com/matteodellamico/4451520
## a little faster than shortest1
def shortest2(n, edges):
    import priority_dict

    def solution(v, back):
        if v == start: return [v]
        return solution(back[v],back)+[v]

    edge = defaultdict(set)
    for (u,v,w) in edges:
        edge[u].add((v,w))
        edge[v].add((u,w))  
    start, end = 0, n-1
    # init : put start to the heap, O(1), but push its neighbors later one by one, O(n1logn1)
    dic = priority_dict.priority_dict()     # dic[u]:(dist,u,last), means the dist from start to u, and last of u is last
    dic[start] = (0,-1)
    back = {}
    global npop, npush
    npop,npush = 0,0
    while dic:
        u, (w0, prev) = dic.pop_smallest()
        npop += 1
        back[u] = prev
        if u == end: return w0, solution(end,back)
        for v, w in edge[u]:  
            if v in back: continue  # v not popped yet
            w1 = w+w0
            if v in dic and w1 >= dic[v][0]: continue
            dic[v] = (w1,u)#dic.__setitem__(v,w1) # v in the queue, or v not visitted
            npush += 1
    return None

'''

## O((E+E)logE), heap
## 0.316 s on flip test
def shortest(n, edges):
    import heapq

    def solution(v, back):
        if v == start: return [v]
        return solution(back[v],back)+[v]

    edge = defaultdict(set)
    back = {}
    d    = defaultdict(lambda: 1<<30)
    for (u,v,w) in edges:
        edge[u].add((v,w))
        edge[v].add((u,w))  
    start, end = 0, n-1
    global npop, npush
    npop,npush = 0,0
    # init : put start to the heap, O(1), but push its neighbors later one by one, O(n1logn1)
    h = [(0,start,-1)]  # (dist,node,prev)
    while len(h):
        dist, u, prev = heapq.heappop(h)
        npop += 1
        if u in back: continue
        back[u] = prev
        if u == end: return dist, solution(end,back)
        for v, w in edge[u]:
            if v not in back:          # v not popped yet   
                if dist+w < d[v]:
                    heapq.heappush(h,(dist+w, v, u))
                    d[v] = dist+w
                    npush += 1
    return None


npop,npush = 0, 0


if __name__ == "__main__":

    print(shortest(4, [(0,1,1), (0,2,5), (1,2,1), (2,3,2), (1,3,6)]))
    # (4, [0,1,2,3])
    print(shortest(5,[(0,2,24),(0,4,20),(3,0,3),(4,3,12)]))
    #(15, [0, 3, 4])

    import sys
    import pdb
    #sys.path.append("/nfs/farm/classes/eecs/winter2018/cs519-010/include")
    SEED, MinDist, MaxDist = 1, 1, 100
    def generate_seq(k,length,seed): import random; random.seed(seed); return [tuple(sorted(random.sample(range(k),2))+[random.randint(MinDist,MaxDist)]) for _ in range(length)]  # (5,10)
    #tuple1 = generate_seq(10,50,1)
    #dense_tuples = generate_seq(1000, 50000, 1)
    dense_tuples = generate_seq(1000, 1000000, SEED)
    VEset = ((1000,5000),(1000,10000),(1000,50000),(1000,500000),(1000,1000000))
    print("see: {}, Weight_Range: {}~{}\n".format(SEED,MinDist,MaxDist))
    for V, E in VEset:
        print("V={}, E={}".format(V, E))
        t1 = time.time()
        res = shortest1(V, dense_tuples[:E])
        print("decrease-key_DIY:{0}, time {1:.3f}, pop:{2}, push:{3}".format(res,time.time()-t1,npop,npush))
        
        t1 = time.time()
        res = shortest(V, dense_tuples[:E])
        print("heappush-only:   {0}, time {1:.3f}, pop:{2}, push:{3}".format(res,time.time()-t1,npop,npush))
        
        t1 = time.time()
        res = shortest2(V, dense_tuples[:E])
        print("heapdict_new:    {0}, time {1:.3f}, pop:{2}, push:{3}\n".format(res,time.time()-t1,npop,npush))
   
        #pdb.set_trace()
    '''
    tuples_1 = generate_seq(5000, 50000, 1)
    tuples_2 = generate_seq(5000, 50000, 4)
    V,E = 5000, 50000
    t1 = time.time()
    print(shortest(V, tuples_1))
    print("V={}, E={}, total time {}".format(V, E,time.time()-t1))

    V,E = 5000, 50000
    t1 = time.time()
    print(shortest(V, tuples_2))
    print("V={}, E={}, total time {}".format(V, E,time.time()-t1))
    '''
