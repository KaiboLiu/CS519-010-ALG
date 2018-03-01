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

if __name__ == "__main__":
    print(order(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6), (5,7)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(order(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6),(5,6),(5,6), (5,7)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(order(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6),(5,6),(5,6), (5,7),(9,10)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(order(8, [(0,2), (1,2), (2,3), (2,4), (4,3), (3,5), (4,5), (5,6), (5,7)]))
    #[0, 1, 2, 4, 3, 5, 6, 7]
    print(order(4, [(0,1), (1,2), (2,1), (2,3)]))
    #None






