# CS519-010-Algorithms    
![](https://img.shields.io/badge/language-python-orange.svg) ![](http://progressed.io/bar/100?title=completed) [![codebeat badge](https://codebeat.co/badges/32258840-1453-4d3b-93fd-cd87c7dc8f8a)](https://codebeat.co/projects/github-com-kaiboliu-cs519-010-alg-master)   
  
- [homeworks](#hw1-python-3-qsort-bst-and-qselect)  
- [sort](#sort)  
- [heap](#heap)  
- [DP and Graph](#dp-and-graph)  
- [knapsack](#knapsack)  
- [BFS and DFS](#bfs-and-dfs)  
- [graph algorithm comparison](#graph-algorithm-comparison)  
- [priority queue(PQ) implememtations for Dijkstra](#priority-queuepq-implememtations-for-dijkstra)  
  
  
### HW1: Python 3, qsort, BST, and qselect   
[code and description](./hw1)   [10/10 cases] Total Time: 0.083 s  
### HW2: Divide-n-conquer: mergesort, number of inversions, longest path   
[code and description](./hw2)  [10/10 cases] Total Time: 0.377 s  
### HW3: K closest numbers; Two Pointers   
[code and description](./hw3)  [10/10 cases] Total Time: 0.276 s  
### HW4: Priority Queue and Heaps   
[code and description](./hw4)  [10/10 cases] Total Time: 0.288 s  
### HW5: DP (part 1: simple)   
[code and description](./hw5)  [10/10 cases] Total Time: 0.009 s  
### HW6: DP (part 2)   
[code and description](./hw6)  [10/10 cases] Total Time: 0.067 s  
### HW7: Void (Midterm Week)   
### HW8: DP (part 3), Graph Algorithms (part 1)   
[code and description](./hw8)  [10/10 cases] Total Time: 0.269 s  
### HW9: Graph Algorithms (part 2), DP (part 4)    
<!--[code and description](./hw9)-->  
code passed but not uploaded  [10/10 cases] Total Time: 0.769 s
### HW10: Challenge Problem - RNA Structure Prediction (6%)    
<!--[code and description](./rna)-->  
code passed but not uploaded  [25/25 cases] Total Time: 0.582 s
  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)  
  
### sort  
#### 01/11/2018 Thu  
+| qsort | qselect | bsearch |msort  
---|---|---|---|---  
1.divide | O(n) | O(n) |  O(1) |O(1)   
2.conquer | 2x | x |  x | 2x   
3.combine | O(n) | O(1) | O(1) | O(n)   
worst | O(n^2)  | O(n^2) |  O(logn) | O(nlogn)  
best | O(nlogn) | O(n)| O(logn) | O(nlogn)  
ave | O(nlogn) | O(n) | O(logn) | O(nlogn)  
  
list in `python` is more like vectore in `C++`, the combination `list+list` costs O(n)  
  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)  
  
### heap  
#### 01/25/2018 Thu  
+| sorted<br>array | unsorted<br>array | (binary)<br>heap | sorted<br>linked list | unsorted<br>linked list | reverse-<br>sorted array  
---|---|---|---|---|---|---  
insert | O(n) | O(1) | O(logn) |  O(n) |O(1) | O(n)  
pop-min | O(n) | O(n) | O(logn) |  O(1)|O(n) | O(1)  
peak | O(1) | O(n) | O(1) | O(1) | O(n) | O(1)  
decrease-key | O(n) | O(n) | O(logn) |  
heapify |O(nlogn)|O(1)|O(n)|O(nlogn)|O(1)|O(nlogn)  
  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)  
  
  
### DP and graph  
#### 02/08/2018 Thu
+| optimization | summary  
---|---|---  
graph | MIS<br> max,min<br>maxmin<br>Unbunded | (sum, expectation)<br>Fib<br>bitstrings   
hyperGraph | matrix-chain | # of BSTs  
  
- Number of n-node BSTs problem is a hyperpraph problem  
  
![](./img/graph.png)  
  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)   
  
### knapsack  
#### 02/13/2018 Tue  
knapsack problem(W, vi,wi,[ci]):  
- 0-1 knapsack  
- Unbunded knapsack  
- Bouded knapsack  
  
All the weights are intergers  
  
##### 1. Unbunded knapsack  
- approach:  
1. Subproblem    
    opt[x]: the subsolution for a bag of x  
1.  Recurrence    
    opt[x]=max{ **opt[x-w[i]]+v[i]** }, i=0..n-1 and x>=w[i]  
1. base case  
    opt[0] = 0  
- Unbunded is a graph problem  
    - time  = E(edges) = O(nW)  
    - space = V(node) = O(W)  
- topological order in graph  
- recursive method(top-down) can automaticly avoid useless value x's without gcd  
  
##### 2. 0-1 knapsack  
- approach:  
1. Subproblem    
    opt[i][x]: opt value for a bag of x, **using** items **0~i**  
1.  Recurrence    
    opt[i][x]=max{ **opt[i-1][x-w[i]]+v[i], opt[i-1][x]** }, i=0~n-1 and x>=w[i]    
    max { choose i, not choose i }  
1. base case  
    - opt[i][0] = 0, i=0~n-1  
    - opt[-1][x] = 0, x=0~W    
- Bounded is a graph problem    
    - time  = E(edges) = O(nW)    
    - space = V(node) = O(nW)  
- 2 nested for loops(i,x), no matter the order of i/x  
- in top-down method, order doesn't matter  
  
![](./img/knapsack.png)  
  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)  
  
  
### BFS and DFS  
#### 03/01/2018 Thu  
+| BFS | DFS  
---|---|---  
structure| queue | stack  
topological order| bottom-up| top-down  
start from| source| sink  
  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)  
  
  
### graph algorithm comparison  
#### 03/01/2018 Thu  
+| Viterbi | Dijkstra
---|---|---|
restriction| DAG<br>(**BIG restriction**) | non-gegative weights
advantage| fast | works in undirected graph<br>works in acyclic/cylic gragh<br>could have early termination
usage| longest/shortest/<br>number/minmax | shortest path <br>single source (***s*** to any)|
implementation| topological sort+<br>BFS(**queue**) | best-first<br>(**priority** queue) <br>with **decrease key**
time complexity | ![O(V+E)](https://img.shields.io/badge/O-V+E-orange.svg) | ![O((V+E)logV)](https://img.shields.io/badge/O-(V+E)logV-orange.svg)  
common| coin problem, TSP | coin problem, TSP   
  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)  
  
  
### priority queue(PQ) implememtations for Dijkstra  
#### 03/06/2018 Tue  
  
- make your window of browser ![](https://img.shields.io/badge/as-wide-brightgreen.svg) as you can

+| PQ<br>(heapdict)| PQ<br>(hash) | PQ<br>(heap) |PQ<br>(unsorted list)
---|---|---|---|---
implementation| binary heap<br>(heapdict)|hash | binary heap| unsorted list
operatrions|pop-min: logV<br>push: logV <br> decrease-key: logV | pop-min: V<br> push: O(1) <br> decrease-key: O(1) | pop-min: logE<br>push: logE <br> decrease-key: logE | pop-min: V<br> push: O(1) <br> decrease-key: V
time complexity |![O((V+E)logV)](https://img.shields.io/badge/O-(V+E)logV-orange.svg)  ↘| ![O(V^2+E)](https://img.shields.io/badge/O-V^2+E-orange.svg) ↓ | ![O((V+E)logE)](https://img.shields.io/badge/O-(V+E)logE-orange.svg)  ↘ | ![V^2+EV](https://img.shields.io/badge/O-V^2+EV-orange.svg) ↓
while PQ not empty:<br> 1. u = pop()<br> 2. for each u->v in E:<br>2.1 decrease-key|V -----------→ **VlogV**<br>logV --------↗ **+**<br>e---→ elogV → **ElogV**<br>logV↗|V ---→ **V^2**<br>V ---↗ **+**<br>e→ e → **E**<br>1 ↗ | V -----------→ **VlogE**<br>logE --------↗ **+**<br>e---→ elogV → **ElogE**<br>logE↗ | V ---→ **V^2**<br>V ---↗ **+**<br>e→eV→**EV**<br>V ↗ 
usage|sparse map<br>E~V|dense map<br>E~ ϴ(V^2)
dense<br>E~ ϴ(V^2)|V^2logV|V^2 (★)| V^2logV | V^3
sparse<br>E~V|VlogV (★)|V^2 | VlogV |V^2
sparse<br>E~VlogV|Vlog^2(V) (★)|V^2

  
[***Back*** to Contents ***CS 519-010***](#cs519-010-algorithms)  


### RNA problem
#### k-best
![tree structure for k-best](./img/k-best%20tree.png)