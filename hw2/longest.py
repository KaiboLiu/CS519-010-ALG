def Lpath(tree):
	if tree == []: return -1,0
	if tree[0] == [] and tree[2] == []: return 0,0

	l_dep, l_path = Lpath(tree[0])
	r_dep, r_path = Lpath(tree[2])
	
	return max(l_dep,r_dep)+1, max(l_dep+r_dep+2, l_path, r_path)  #return no_this_node, pass_this_node
	### return a,b is equivalent to return (a,b), it's a tuple, not list

def longest(tree):
	dep, path = Lpath(tree)
	return max(dep, path)


if __name__ == "__main__":
	print('longest([[], 1, []]):')
	print(longest([[], 1, []]))

	print('longest([[[], 1, []], 2, [[], 3, []]]):')
	print(longest([[[], 1, []], 2, [[], 3, []]]))

	print('longest([[[[], 1, []], 2, [[], 3, []]], 4, [[[], 5, []], 6, [[], 7, [[], 9, []]]]]):')
	print(longest([[[[], 1, []], 2, [[], 3, []]], 4, [[[], 5, []], 6, [[], 7, [[], 9, []]]]]))

	print('longest([[], 2, [[[[], 6, []], 4, []], 3, [[], 5, [[], 7, []]]]]):')
	print(longest([[], 2, [[[[], 6, []], 4, []], 3, [[], 5, [[], 7, []]]]]))