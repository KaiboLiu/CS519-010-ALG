'''
Developer: Kaibo(lrushx)
Email: liukaib@oregonstate.edu
Process Time: Mar 1, 2018
'''

from collections import defaultdict
import pdb

class keyPQ():  # decrease-key priority queue
    def __init__(self, h=[]):
        self.heap = h           # list of [weight, V] in heap
        self.len  = len(h)
        self.popped = set()
        self.idx  = defaultdict(lambda:-1)
        for i,(_,v) in enumerate(h): self.idx[v] = i
        self.heapify()

    def heapify(self):
        i0 = self.len // 2
        for i in range(i0,-1,-1): 
            self.sink(i)

    def push(self, item):
        self.heap.append(item)
        self.idx[item[1]] = self.len
        self.rise(self.len)
        self.len += 1
        #pdb.set_trace()

    def pop(self):
        if self.len == 0: return None
        self.len -= 1
        #self.switch(self.heap[0],self.heap[-1],0,self.len)
        self.switch(0,self.len)
        top = self.heap.pop()
        self.popped.add(top[1])
        self.sink(0)
        return top

    def sink(self, i):
        l, r = i+i+1, i+i+2
        if l >= self.len: return
        if r >= self.len and self.heap[i][0] > self.heap[l][0]:
            #self.switch(self.heap[i], self.heap[l], i, l)
            self.switch(i, l)
            self.sink(l)
        if r < self.len:
            minChild = l if self.heap[l][0] < self.heap[r][0] else r
            if self.heap[i][0] > self.heap[minChild][0]:
                #self.switch(self.heap[i], self.heap[minChild], i, minChild)
                self.switch(i, minChild)
                self.sink(minChild)

    def rise(self, i):
        if i == 0: return 
        parent = (i-1)//2
        if self.heap[i][0] < self.heap[parent][0]:
            #self.switch(self.heap[i], self.heap[parent], i, parent)
            self.switch(i, parent)
            self.rise(parent)

    def switch(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        #[w1, v1], [w2, v2] = a1, a2
        #a1, a2 = [w2, v2], [w1, v1]
        self.idx[self.heap[i][1]], self.idx[self.heap[j][1]] = i, j 

    def decreaseKey(self, i, w):
        #if w >= self.heap[i][0]: return
        self.heap[i][0] = w
        self.rise(i)


def shortest(n, edges):

    def solution(v, back):
        if v == start: return [0]
        res = solution(back[v],back)
        res.append(v)
        return res

    weight, edge = defaultdict(lambda: 100000000), defaultdict(list)
    dist, back = defaultdict(lambda:-1), defaultdict(int)
    for (u,v,w) in edges:
        weight[u,v] = weight[v,u] = w
        edge[u].append(v)
        edge[v].append(u)

    start, end = 0, n-1
    q = keyPQ([[0,start]])
    while q.len:
        w0, u = q.pop()
        for w,v in q.heap:
            w1 = weight[u,v]+w0
            if w1 < w:
                q.decreaseKey(q.idx[v],w1)
                dist[v], back[v] = w1, u
        for v in edge[u]:       # the rest nodes linked to u, which are not in the queue
            if v not in q.idx:
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