# CS519-010-ALG  
![](https://img.shields.io/badge/language-python-orange.svg)  
homeworks on CS519-010 Algorithm       
## HW1: Python 3, qsort, BST, and qselect 
[code and description](./hw1) 
## HW2: Divide-n-conquer: mergesort, number of inversions, longest path 
[code and description](./hw2)
## HW3: K closest numbers; Two Pointers 
[code and description](./hw3)
## HW4: Priority Queue and Heaps 
[code and description](./hw4)
## HW5: DP (part 1: simple) 
[code and description](./hw5)
## HW6: DP (part 2) 
[code and description](./hw6)
## HW7: Void (Midterm Week) 
## HW8: DP (part 3), Graph Algorithms (part 1) 
[code and description](./hw8)
## HW9: Graph Algorithms (part 2), DP (part 4)  
[code and description](./hw9)
## HW10: Challenge Problem - RNA Structure Prediction (6%). 
[code and description](./rna)

-| Viterbi | Dijkstra
---|---|---|
restriction| DAG<br>(**BIG restriction**) | non-gegative weights
advantage| fast | works in undirected graph<br>works in acyclic/cylic gragh<br>could have early termination
usage| longest/shortest/<br>number/minmax | shortest path <br>single source (***s*** to any)|
implementation| topological sort+<br>BFS(**queue**) | best-first<br>(**priority** queue) <br>with **decrease key**
time complexity | O(V+E) | O((V+E)logV)
common| coin problem | coin problem 


-| PQ(heap)| PQ(hash)
---|---|---
implementation| binary heap<br>(heapdict)|hash
operatrions|pop-min: logV<br>push: logV <br> decrease-key: logV | pop-min: V<br> push: O(1) <br> decrease-key: O(1))
time complexity |O((V+E)logV)| O(V^2+E)
while PQ not empty<br> 1. u = pop()<br> 2. for each u->v<br>2.1 decrease-key|V -----------→ **VlogV**<br>logV --------↗ **+**<br>e---→ elogV → **ElogV**<br>logV↗|V ---→ **V^2**<br>V ---↗ **+**<br>e→ e → **E**<br>1 ↗
usage|sparse map<br>E~V|dense map<br>E~V^2
dense<br>E~V^2|V^2logV|V^2 (★)
sparse<br>E~V|VlogV (★)|V^2
sparse<br>E~VlogV|Vlog^2(V) (★)|V^2
