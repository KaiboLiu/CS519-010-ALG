from collections import defaultdict
from topol import order

def longest(n, edges):
    def solution(v, back, res=[]):
        if back[v] > -1:
            solution(back[v], back)

        res.append(v)
        return res
        
    nodes = order(n, edges) # O(V+E)
    if nodes is None: return None
    succ = defaultdict(list)
    for (u,v) in edges:
        succ[u].append(v)
    opt, back, l = defaultdict(int), defaultdict(lambda:-1), 0
    for u in nodes: # O(E)
        for v in succ[u]:
            if opt[u] + 1 > opt[v]:
                opt[v], back[v] = opt[u]+1, u
                if opt[v] > l:
                    l = opt[v]
                    end = v
    return l, solution(end, back)

if __name__ == "__main__":
    
    print(longest(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6), (5,7)]))
    # (5, [0, 2, 3, 4, 5, 6])
    print(longest(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6),(5,6),(5,6), (5,7)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(longest(8, [(0,2), (1,2), (2,3), (2,4), (3,4), (3,5), (4,5), (5,6),(5,6),(5,6), (5,7),(9,10)]))
    #[0, 1, 2, 3, 4, 5, 6, 7]
    print(longest(8, [(0,2), (1,2), (2,3), (2,4), (4,3), (3,5), (4,5), (5,6), (5,7)]))
    #[0, 1, 2, 4, 3, 5, 6, 7]
    print(longest(4, [(0,1), (1,2), (2,1), (2,3)]))
    #None
