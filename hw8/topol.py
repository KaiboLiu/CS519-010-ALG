from collections import defaultdict
from heapq import heapify, heappop

def order(n, edges):
    npre, nodes, to = defaultdict(int), [], defaultdict(lambda:[])
    for i, (u,v) in enumerate(edges):
        npre[u] = npre[u]
        npre[v] += 1
        to[u].append(v)

    for v in npre:
        nodes.append([npre[v],v])
    res = []
    heapify(nodes)

    while nodes != []:
        if nodes[0][0] > 0:
            return None
        _, u = heappop(nodes)
        res.append(u)
        for v in to[u]:
            idx = nodes.index([npre[v],v])
            npre[v] -= 1
            nodes[idx][0] -= 1
        heapify(nodes)
    return res


if __name__ == "__main__":
    print(order(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6), (5,7)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(order(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6),(5,6),(5,6), (5,7)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(order(8, [(0,2), (1,2), (2,3), (2,4), (4,3), (3,5), (4,5), (5,6), (5,7)]))
    #[0, 1, 2, 4, 3, 5, 6, 7]
    print(order(4, [(0,1), (1,2), (2,1), (2,3)]))
    #None






