'''
Developer: Kaibo(lrushx)
Email: liukaib@oregonstate.edu
Process Time: Mar 6, 2018
'''
from collections import defaultdict

# top-down, bit, int2set
def tsp10(n, edges):      
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
    Next, V, res = start, V+1, []
    while Next != -1:
        res.append(Next)
        V -= (1<<Next)
        Next = arrow[Next, V]
    return res_dist, res
    

# top-down, bit
def tsp11(n, edges):
    def _dist(i, V):
        # dist[i,V] = min { weight[i,k] + dist[k, V-<k>] }, k in V, 'V-<k>' means the set V without k
        # I used bit presentation for V, so V-<k> is V-(1<<k)
        if (i, V) in dist: return dist[i,V]
        for k in edge[i]:
            if (1<<k & V):
                dist1 = weight[i,k]+_dist(k, V-(1<<k))
                if dist1 < dist[i,V]:
                    arrow[i, V] = k
                    dist[i,V] = dist1
        return dist[i,V]

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
    res_dist = _dist(0, V)  # Let's roll
    Next, V, res = start, V+1, []
    while Next != -1:
        res.append(Next)
        V -= (1<<Next)
        Next = arrow[Next, V]
    return res_dist, res

def tsp1(n, edges):     # viterbi, bit
    #opt is a list, opt[i] is a dict for node i, (Vset, last):(dist, back)

    edge = defaultdict(lambda: defaultdict(lambda: float('inf')))
    for u,v,w in edges:
        edge[u][v] = min(edge[u][v], w) # possible duplicate edges
        edge[v][u] = min(edge[v][u], w) # undirected
    for u in range(1,n): edge[u][n] = edge[u][0]    # clone a dummy sink n, which is 0

    opt = [for _ in range(n+1)]


if __name__ == "__main__":

    import time
    t0 = time.time()
    print(tsp(4, [(0,1,1), (0,2,5), (1,2,1), (2,3,2), (1,3,6)]))
    print('{} cities, time: {}\n'.format(4,time.time()-t0))
    # (14, [0,1,3,2,0])


    t0 = time.time()
    print(tsp(4, [(0,1,1), (0,2,5), (1,2,1), (2,3,2), (1,3,6), (3,0,1)]))
    print('{} cities, time: {}\n'.format(4,time.time()-t0))
    # (5, [0,1,2,3,0])

    t0 = time.time()
    print(tsp(11, [(0,1,29),(0,2,20),(0,3,21),(0,4,16),(0,5,31),(0,6,100),(0,7,12),(0,8,4),(0,9,31),(0,10,18),
                (1,2,15),(1,3,29),(1,4,28),(1,5,40),(1,6,72),(1,7,21),(1,8,29),(1,9,41),(1,10,12),
                (2,3,15),(2,4,14),(2,5,25),(2,6,81),(2,7,9),(2,8,23),(2,9,27),(2,10,13),
                (3,4,4),(3,5,12),(3,6,92),(3,7,12),(3,8,25),(3,9,13),(3,10,25),
                (4,5,16),(4,6,94),(4,7,9),(4,8,20),(4,9,16),(4,10,22),
                (5,6,95),(5,7,24),(5,8,36),(5,9,3),(5,10,37),
                (6,7,90),(6,8,101),(6,9,99),(6,10,84),
                (7,8,15),(7,9,25),(7,10,13),
                (8,9,35),(8,10,18),
                (9,10,38)]))
    print('{} cities, time: {}\n'.format(11,time.time()-t0))
    # (253, [0, 8, 10, 1, 6, 2, 5, 9, 3, 4, 7, 0])
    # (Viterbi: 0.0s; Dijkstra: 0.3s)

    import random
    random.seed(2)
    n, m = 16, 100
    edges = [(random.randint(0,n-1), random.randint(0,n-1), random.randint(0,5)) for _ in range(m)] + \
            [(random.randint(0,n-1), random.randint(0,n-1), random.randint(6,10)) for _ in range(m)] 
    t0 = time.time()
    print(tsp(n,edges))
    print('{} cities, time: {}'.format(n,time.time()-t0))
    #(6, [0, 4, 8, 14, 7, 5, 10, 3, 13, 12, 9, 11, 15, 6, 2, 1, 0])
    #(Viterbi: 2.1s, Dijkstra: 0.9s)