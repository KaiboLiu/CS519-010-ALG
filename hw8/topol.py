from collections import defaultdict


def order1(n, edges):
    from heapq import heapify, heappop
    degree, nodes, succ = defaultdict(int), [], defaultdict(list)
    for i, (u,v) in enumerate(edges):
        degree[u] = degree[u]
        degree[v] += 1
        succ[u].append(v)

    for v in degree:
        nodes.append([degree[v],v])
    res = []
    heapify(nodes)

    while nodes != []:
        if nodes[0][0] > 0:
            return None
        _, u = heappop(nodes)
        res.append(u)
        for v in succ[u]:
            idx = nodes.index([degree[v],v])
            degree[v] -= 1
            nodes[idx][0] -= 1
        heapify(nodes)
    return res


## BFS, use list as a queue
def order(n, edges):
    degree, nodes, succ = defaultdict(int), [], defaultdict(list)
    for i, (u,v) in enumerate(edges):
        degree[u] = degree[u]
        degree[v] += 1
        succ[u].append(v)

    res, nodes, used, i = [], [], set(), 0   # i is the open pointer in queue 'nodes'
    for u in succ:
        if degree[u] == 0: 
            nodes.append(u)
            used.add(u)
    while i < len(nodes):
        u = nodes[i]
        res.append(u)
        if degree[u]: return None
        i += 1
        for v in succ[u]:
            degree[v] -= 1
            if degree[v] == 0:
                nodes.append(v)
    if i < len(degree): return None            
    return res


## added on 03/20/2018
## DFS
def order_DFS1(n, edges):
    def DFS(v,res): 
        color[v] = -1
        print('v:',v)
        for u in pred[v]:
            if color[u] < 0: continue
            degree[u] -= 1
            if degree[u] == 0:
                DFS(u,res)
                res.append(u)
        
        #print(res)

    degree, pred = defaultdict(int), defaultdict(list)
    color = defaultdict(int)    # color: -1:black/popped, 0: white/not_visited, 1: grey/visited
    res = []   # i is the open pointer in queue 'nodes'

    for (u,v) in edges:
        degree[v] = degree[v]
        degree[u] += 1
        pred[v].append(u)
    for u in range(n):      # add a sink
        degree[u] += 1
        pred[n].append(u)
    #print(degree)
    DFS(n,res)
    print(res)
    return res if len(res) == n else None

## added on 03/16/2018
## DFS
def order_DFS2(n, edges):
    def DFS(v,res): 
        if color[v] == 1: return False  # visit a grey one twice
        color[v] = 1
        for u in pred[v]:
            if color[u] >= 0:
                if not DFS(u,res): return False
        if degree[v] == 0:
            res.append(v)
            color[v] = -1
            for v1 in succ[v]:
                if color[v1] >= 0: degree[v1] -= 1
        return True

    for i in range(n):
        edges.append((i,n))

    degree, pred, succ = defaultdict(int), defaultdict(list), defaultdict(list)
    color = defaultdict(int)    # color: -1:black/popped, 0: white/not_visited, 1: grey/visited
    res = []   # i is the open pointer in queue 'nodes'
    for (u,v) in edges:
        degree[u] = degree[u]
        degree[v] += 1
        pred[v].append(u)
        succ[u].append(v)   
    acyclic = DFS(n,res)
    return res[:-1] if acyclic else None


## added on 03/20/2018
## DFS
def order_DFS3(n, edges):
    def DFS(v,res): 
        if color[v] == 1: return False  # visit a grey one twice
        color[v] = 1
        for u in pred[v]:
            if color[u] >= 0:
                if not DFS(u,res): return False
        if degree[v] == 0:
            res.append(v)
            color[v] = -1
            for v1 in pred[v]:
                if color[v1] >= 0: degree[v1] -= 1
        return True

    for i in range(n):
        edges.append((i,n))

    degree, pred = defaultdict(int), defaultdict(list)
    color = defaultdict(int)    # color: -1:black/popped, 0: white/not_visited, 1: grey/visited
    res = []   # i is the open pointer in queue 'nodes'
    for (u,v) in edges:
        degree[v] = degree[v]
        degree[u] += 1
        pred[v].append(u)
    acyclic = DFS(n,res)
    return res[:-1] if acyclic else None


if __name__ == "__main__":
    print(order_DFS3(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6), (5,7)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(order_DFS3(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6),(5,6),(5,6), (5,7)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(order_DFS3(11, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6),(5,6),(5,6), (5,7),(9,10)]))
    #[0, 1, 9, 2, 10, 3, 4, 5, 6, 7]
    print(order_DFS3(8, [(0,2), (1,2), (2,3), (2,4), (4,3), (3,5), (4,5), (5,6), (5,7)]))
    #[0, 1, 2, 4, 3, 5, 6, 7]
    print(order_DFS3(4, [(0,1), (1,2), (2,1), (2,3)]))
    #None






