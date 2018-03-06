# CS519-010-Algorithms  
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
<!--[code and description](./hw9)-->
code passed but not uploaded
## HW10: Challenge Problem - RNA Structure Prediction (6%)  
<!--[code and description](./rna)-->
code finished but not uploaded


### sort
#### 01/11/2018 Thu
+| qsort | qselect | bsearch |msort
---|---|---|---|---
1. divide | O(n) | O(n) |  O(1) |O(1) 
2. conquer | 2x | x |  x | 2x 
3. combine | O(n) | O(1) | O(1) | O(n) 
worst | O(n^2)  | O(n^2) |  O(logn) | O(nlogn)
best | O(nlogn) | O(n)| O(logn) | O(nlogn)
ave | O(nlogn) | O(n) | O(logn) | O(nlogn)

list in `python` is more like vectore in `C++`, the combination `list+list` costs O(n)

[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms)

### heap
#### 01/25/2018 Thu
+| sorted<br>array | unsorted<br>array | (binary)<br>heap | sorted<br>linked list | unsorted<br>linked list | reverse-<br>sorted array
---|---|---|---|---|---|---
insert | O(n) | O(1) | O(logn) |  O(n) |O(1) | O(n)
pop-min | O(n) | O(n) | O(logn) |  O(1)|O(n) | O(1)
peak | O(1) | O(n) | O(1) | O(1) | O(n) | O(1)
decrease-key | O(n) | O(n) | O(logn) |
heapify |O(nlogn)|O(1)|O(n)|O(nlogn)|O(1)|O(nlogn)

[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms)


### DP and graph
+| optimization | summary
---|---|---
graph | MIS<br> max,min<br>maxmin<br>Unbunded | (sum, expectation)<br>Fib<br>bitstrings 
hyperGraph | matrix-chain | # of BSTs

- Number of n-node BSTs problem is a hyperpraph problem
```
graph TD
C1((i-1))-->P((n))
C2((n-i))-->P((n))
A((u))-->B((v))
subgraph graph problem
A
B
end
subgraph hyperGraph problem
C1
C2
P
end
```

[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms) 

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
1. base caser
    opt[0] = 0
- Unbunded is a graph problem
    - time  = E(edges) = O(nW)
    - space = V(node) = O(W)
- topological order in graph
- recursive method(top-down) can automaticly avoid useless value x's without gcd

[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms) 

##### 2. 0-1 knapsack
- approach:
1. Subproblem  
    opt[i][x]: opt value for a bag of x, **using** items **0~i**
1.  Recurrence  
    opt[i][x]=max{ **opt[i-1][x-w[i]]+v[i], opt[i-1][x]** }, i=0..n-1 and x>=w[i]  
    max { choose i, not choose i }
1. base case
    opt[i][0] = 0, i=0~n-1
    opt[-1][x] = 0, x=0~W
- Bounded is a graph problem
    - time  = E(edges) = O(nW)
    - space = V(node) = O(nW)
- 2 nested for loops(i,x), no matter the order of i/x
- in top-down method, order doesn't matter

```
graph TD
I1(opt <b>x-w1</b>)-->|+v1|x2(opt <b>x</b>)
I2(opt <b>x-w2</b>)-->|+v2|x2
I3(...)-->x2
I4(opt <b>x-wn</b>)-->|+vn|x2

A(opt <b>i-1, x-wi</b>)-->|+vi|x1(opt <b>i, x</b>)
C(opt <b>i-1, x</b>)-->x1

subgraph  Unbunded knapsack
x2
I1
I2
I3
I4
end
subgraph 0-1 knapsack
x1
A
C
end

```


[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms)


### BFS and DFS
#### 03/01/2018 Thu
+| BFS | DFS
---|---|---
structure| queue | stack
topological order| bottom-up| top-down
start from| source| sink

[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms)


### graph algorithm comparison
#### 03/01/2018 Thu
+| Viterbi | Dijkstra
---|---|---|
restriction| DAG<br>(**BIG restriction**) | non-gegative weights
advantage| fast | works in undirected graph<br>works in acyclic/cylic gragh<br>could have early termination
usage| longest/shortest/<br>number/minmax | shortest path <br>single source (***s*** to any)|
implementation| topological sort+<br>BFS<br>(**queue**) | best-first<br>(**priority** queue) <br>with **decrease key**
time complexity | O(V+E) | O((V+E)logV)
common| coin problem | coin problem 

[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms)


### priority queue(PQ) implememtations for Dijkstra
#### 03/06/2018 Tue

+| PQ(heap)| PQ(hash)
---|---|---
implementation| binary heap<br>(heapdict)|hash
operatrions|pop-min: logV<br>push: logV <br> decrease-key: logV | pop-min: V<br> push: O(1) <br> decrease-key: O(1)
time complexity ↓ |O((V+E)logV) ↘| O(V^2+E) ↓
while PQ not empty<br> 1. u = pop()<br> 2. for each u->v<br>2.1 decrease-key|V -----------→ **VlogV**<br>logV --------↗ **+**<br>e---→ elogV → **ElogV**<br>logV↗|V ---→ **V^2**<br>V ---↗ **+**<br>e→ e → **E**<br>1 ↗
usage|sparse map<br>E~V|dense map<br>E~V^2
dense<br>E~V^2|V^2logV|V^2 (★)
sparse<br>E~V|VlogV (★)|V^2
sparse<br>E~VlogV|Vlog^2(V) (★)|V^2

[***Back*** to Contents ***CS 519-010***](#cs-519-010-algorithms)
