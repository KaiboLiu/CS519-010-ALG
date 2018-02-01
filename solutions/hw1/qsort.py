#!/usr/bin/env python3

import sys

def sort(a):
    if a == []:
        return []
    pivot = a[0]
    left = [x for x in a if x < pivot]
    right = [x for x in a[1:] if x >= pivot]
    return [sort(left)] + [pivot] + [sort(right)]

def sorted(tree):
    return [] if tree == [] else sorted(tree[0]) + [tree[1]] + sorted(tree[2])

def _search(tree, x):
    if tree == [] or tree[1] == x:
        return tree
    return _search(tree[0], x) if x < tree[1] else _search(tree[2], x)

def search(tree, x):
    return _search(tree,x) != []

def insert(tree, x):
    r = _search(tree, x)
    if r == []:
        r += [[], x, []]

if __name__ == '__main__':
    tree = sort([4,2,6,3,5,7,1,9])
    print(tree)
    t1 = sorted(tree)
    print(t1)
    
    print(search(tree,6))
    print(search(tree,6.5))
    insert(tree,6.5)
    print(tree)
    insert(tree,3)
    print(tree)
    tree = sort([4,2,6,3,5,7,1,9])        # starting from the initial tree
    print(_search(tree, 3))
    print(_search(tree, 0))
    print(_search(tree, 6.5))
    print(_search(tree, 0) is _search(tree, 6.5))
    print(_search(tree, 0) == _search(tree, 6.5))
