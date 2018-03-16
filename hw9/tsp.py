'''
Developer: Kaibo(lrushx)
Email: liukaib@oregonstate.edu
Process Time: Mar 6, 2018
'''
from collections import defaultdict
import heapq
import time

'''
# top-down, bit, int2set
def tsp_topdown0(n, edges):      
    def init_setV(i, V, n):
        if i == n: return
        v1 = V | (1 << i)   # V + 2^i
        setV[v1] = set(setV[V])
        setV[v1].add(i)
        init_setV(i+1, V, n)
        init_setV(i+1, v1, n)

    def _dist(i, V):
        # dist[i,V] = min { weight[i,k] + dist[k, V-<k>] }, k in V, 'V-<k>' means the set V without k
        # I used bit presentation for V, so V-<k> is V-(1<<k)
        if (i, V) in dist: return dist[i,V]
        for k in setV[V]:
            dist1 = weight[i,k]+_dist(k, V-(1<<k))
            if dist1 < dist[i,V]:
                arrow[i, V] = k
                dist[i,V] = dist1
        return dist[i,V]
    t0 = time.time()
    start, end = 0, n-1
    weight = defaultdict(lambda: 1 << 32)
    for (u,v,w) in edges:
        weight[u,v] = weight[v,u] = min(w,weight[u,v]) 

    setV = defaultdict(set)
    init_setV(1, 0, n)  # city start(0) not in setV, V != 1

    dist, arrow = defaultdict(lambda:1 << 32), defaultdict(lambda: -1)
    # dist[i,V] means the min distance i -> V -> start, V is the bit presentation of city set, setV:: int -> set
    # arrow is the result(fowward track), j=arrow[i,V] means i's next city in V, then the next city is arrow[j, V-(1<<j)]
    for u in range(1,n): 
        dist[u,0] = weight[u, start]
        arrow[u, 0] = start
    
    V = (1<<n)-2            # all nodes except start (0)
    res_dist = _dist(0, V)  # Let's roll
    print('topdown, bit2set, time: {0:.3f}'.format(time.time()-t0))
    Next, V, res = start, V+1, []
    while Next != -1:
        res.append(Next)
        V -= (1<<Next)
        Next = arrow[Next, V]
    return res_dist, res
    

# top-down, bit
def tsp_topdown1(n, edges):
    def _dist(i, V):
        # dist[i,V] = min { weight[i,k] + dist[k, V-<k>] }, k in V, 'V-<k>' means the set V without k
        # I used bit presentation for V, so V-<k> is V-(1<<k)
        if (i, V) in dist: return dist[i,V], 0
        npush = 0
        for k in edge[i]:
            if (1<<k & V):
                lastDist = _dist(k, V-(1<<k))
                dist1 = weight[i,k] + lastDist[0]
                npush += lastDist[1]
                if dist1 < dist[i,V]:
                    arrow[i, V] = k
                    dist[i,V] = dist1
                    npush += 1
        return dist[i,V], npush
    t0 = time.time()
    start, end = 0, n-1
    weight, edge = defaultdict(lambda: 1 << 32), defaultdict(set)
    for (u,v,w) in edges:
        weight[u,v] = weight[v,u] = min(w,weight[u,v]) 
        edge[u].add(v)
        edge[v].add(u)

    dist, arrow = defaultdict(lambda:1 << 32), defaultdict(lambda: -1)
    # dist[i,V] means the min distance i -> V -> start, V is the bit presentation of city set, setV:: int -> set
    # arrow is the result(fowward track), j=arrow[i,V] means i's next city in V, then the next city is arrow[j, V-(1<<j)]
    for u in range(1,n): 
        dist[u,0] = weight[u, start]
        arrow[u, 0] = start
    
    V = (1<<n)-2            # all nodes except start (0)
    res_dist, npush = _dist(0, V)  # Let's roll
    print('topdown, bit, time: {0:.3f}, push: {1}'.format(time.time()-t0,npush+n-1))
    Next, V, res = start, V+1, []
    while Next != -1:
        res.append(Next)
        V -= (1<<Next)
        Next = arrow[Next, V]
    return res_dist, res

def tsp_viterbi(n, edges):     # viterbi, bit
    #opt is a list for topological order of a induced graph, opt[i] is a dict for node i, (nodeset, last):(dist, back)
    #dist is the distance from 0 to last, and visit all the nodes in nodeset, 0-->nodeset(include 0)-->last-->i
    def solution(i,nodeset,j):
        if j == 0: return [0]
        _, last = opt[i][nodeset,j]
        return solution(i-1, nodeset-(1<<j),last)+[j%n]

    t0 = time.time()
    edge = defaultdict(lambda: defaultdict(lambda: float('inf')))
    for u,v,w in edges:
        edge[u][v] = min(edge[u][v], w) # possible duplicate edges
        edge[v][u] = min(edge[v][u], w) # undirected
    for u in range(1,n): edge[u][n] = edge[u][0]    # clone a dummy sink n, which is 0

    opt = [defaultdict(lambda:( float('inf'), None) )for _ in range(n+2)]   # best dist and back together, opt[0] is a dummy source , opt[1] is real node 0
    opt[1][1,0] = (0,None)  # 1: 0000001, node 0 visited
    npush = 0
    for i in range(1,n+1):
        for (nodeset, last),(dist,_) in opt[i].items():
            for j in range(1,n) if i < n else [n]:
                if j in edge[last] and not (1<<j & nodeset):
                    newdis = dist + edge[last][j]
                    newset = 1<<j | nodeset
                    if newdis < opt[i+1][newset,j][0]:
                        opt[i+1][newset,j] = (newdis, last)
                        npush += 1
    fullsetplus = (1<<(n+1)) - 1    # 111...1, n+1 in total
    print('viterbi, bit, time: {0:.3f}, push: {1}'.format(time.time()-t0,npush))
    return opt[n+1][fullsetplus, n][0], solution(n+1,fullsetplus, n)


def tsp_dijk_heapq(n, edges):    # Dijkstra, bit, heapq
    def solution(nodeset, v):
        if nodeset == 1: return [0]
        u = back[nodeset, v]
        return solution(nodeset-(1<<v), u) + [v%n]

    t0 = time.time()
    edge = defaultdict(lambda: defaultdict(lambda: float('inf')))
    for u,v,w in edges:
        edge[u][v] = min(edge[u][v], w) # possible duplicate edges
        edge[v][u] = min(edge[v][u], w) # undirected
    for u in range(1,n): edge[u][n] = edge[u][0]    # clone a dummy sink n, which is 0
    h = [(0, (1,0), None)]  # (dist,(nodeset,last),prev), the best dist for 0->nodeset->last is dist, and we have the prev of last
    back = {}
    npop = npush = 0
    fullset, fullsetplus = (1<<n)-1, (1<<n+1)-1    # + has high priority than <<
    while h:
        dist, (nodeset, u), prev = heapq.heappop(h)
        npop += 1
        if (nodeset, u) in back: continue
        back[nodeset, u] = prev
        if nodeset == fullsetplus: 
            print('Dijkstra, heapq, time: {0:.3f}, push: {1}, pop: {2}'.format(time.time()-t0,npush,npop))
            return dist, solution(nodeset, u)

        for v in range(1,n) if nodeset < fullset else [n]:
            if v in edge[u] and not (1<<v & nodeset):
                newdis = dist + edge[u][v]
                newset = 1<<v | nodeset
                if (newset, v) not in back:    # no need to check this new one is better
                    heapq.heappush(h,(newdis, (newset, v), u))
                    npush += 1

'''

#def tsp_dijk_heapdict(n, edges):    # Dijkstra, bit, heap-dict from from https://gist.github.com/matteodellamico/4451520
def tsp(n, edges):    # Dijkstra, bit, heap-dict from from https://gist.github.com/matteodellamico/4451520
    import priority_dict

    def solution(nodeset, v):
        if nodeset == 1: return [0]
        u = back[nodeset, v]
        return solution(nodeset-(1<<v), u) + [v%n]

    t0 = time.time()
    edge = defaultdict(lambda: defaultdict(lambda: float('inf')))
    for u,v,w in edges:
        edge[u][v] = min(edge[u][v], w) # possible duplicate edges
        edge[v][u] = min(edge[v][u], w) # undirected
    for u in range(1,n): edge[u][n] = edge[u][0]    # clone a dummy sink n, which is 0
    d = priority_dict.priority_dict()
    d[1,0] = (0, None)  # d[nodeset,last] = (dist,prev), the best dist for 0->nodeset->last is dist, and we have the prev of last
    back = {}
    npop = npush = 0
    fullset, fullsetplus = (1<<n)-1, (1<<n+1)-1    # + has high priority than <<
    while d:
        (nodeset,u), (dist,prev) = d.pop_smallest()
        npop += 1
        if (nodeset, u) in back: continue
        back[nodeset, u] = prev
        if nodeset == fullsetplus: 
            print('Dijkstra, heapdict, time: {0:.3f}, push: {1}, pop: {2}'.format(time.time()-t0,npush,npop))
            return dist, solution(nodeset, u)

        for v in range(1,n) if nodeset < fullset else [n]:
            if v in edge[u] and not (1<<v & nodeset):
                newset = 1<<v | nodeset
                if (newset, v) in back: continue
                newdis = dist + edge[u][v]
                if (newset, v) in d and newdis >= d[newset, v][0]: continue
                d[newset, v] = newdis, u
                npush += 1


if __name__ == "__main__":

    import random
    random.seed(2)
    n, m = 16, 100
    randedges = [(random.randint(0,n-1), random.randint(0,n-1), random.randint(0,5)) for _ in range(m)] + \
            [(random.randint(0,n-1), random.randint(0,n-1), random.randint(6,10)) for _ in range(m)] 
    cases = [(4, [(0,1,1), (0,2,5), (1,2,1), (2,3,2), (1,3,6)]),
             # (14, [0,1,3,2,0])
             (4, [(0,1,1), (0,2,5), (1,2,1), (2,3,2), (1,3,6), (3,0,1)]),
             # (5, [0,1,2,3,0])
             (11, [(0,1,29),(0,2,20),(0,3,21),(0,4,16),(0,5,31),(0,6,100),(0,7,12),(0,8,4),(0,9,31),(0,10,18),
                (1,2,15),(1,3,29),(1,4,28),(1,5,40),(1,6,72),(1,7,21),(1,8,29),(1,9,41),(1,10,12),
                (2,3,15),(2,4,14),(2,5,25),(2,6,81),(2,7,9),(2,8,23),(2,9,27),(2,10,13),
                (3,4,4),(3,5,12),(3,6,92),(3,7,12),(3,8,25),(3,9,13),(3,10,25),
                (4,5,16),(4,6,94),(4,7,9),(4,8,20),(4,9,16),(4,10,22),
                (5,6,95),(5,7,24),(5,8,36),(5,9,3),(5,10,37),
                (6,7,90),(6,8,101),(6,9,99),(6,10,84),
                (7,8,15),(7,9,25),(7,10,13),
                (8,9,35),(8,10,18),
                (9,10,38)]),
                # (253, [0, 8, 10, 1, 6, 2, 5, 9, 3, 4, 7, 0])
                # (Viterbi: 0.0s; Dijkstra: 0.3s)
                (n,randedges)
                #(6, [0, 4, 8, 14, 7, 5, 10, 3, 13, 12, 9, 11, 15, 6, 2, 1, 0])
                #(Viterbi: 2.1s, Dijkstra: 0.9s)
            ]

    for n, edges in cases:
        print('\n{} cities'.format(n))
        print(tsp_topdown1(n,edges))
        print(tsp_topdown0(n,edges))
        print(tsp_viterbi(n,edges))
        print(tsp_dijk_heapq(n,edges))
        #print(tsp_dijk_heapdict(n,edges))
        print(tsp(n,edges))

    
    