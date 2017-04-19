'''
Question 1
Given two strings s and t, determine whether some anagram of t is a 
substring of s. For example: if s = "udacity" and t = "ad", then the 
function returns True. Your function definition should look like: 
question1(s, t) and return a boolean True or False.
'''
def is_anagram(s1, s2):
    s1 = list(s1)
    s2 = list(s2)
    s1.sort()
    s2.sort()
    return s1 == s2

def question1(s, t):
    match_length = len(t)
    pattern_length = len(s)
    for i in range(pattern_length - match_length + 1):
        if is_anagram(s[i: i+match_length], t):
            return True
    return False
	
#Test Cases
print(question1('','f'))
#False

print(question1('dormitory','tim'))
#True

print(question1('debit card','debit'))
#True

'''
Question 2
Given a string a, find the longest palindromic substring contained in a. 
Your function definition should look like question2(a), and return a string.
'''
def question2(a):
    string="#"+"#".join(s)+"#"

    i=0
    mxBorder=0                
    mxCenter=0                
    p=[0]*len(string)
    res=[0,0]
    
    while i< len(string):
        if mxBorder>i:            
            p[i]=min(p[2*mxCenter-i],mxBorder-i) 
                                       
        else:
            p[i]=1
    
        while i-p[i]>=0 and i+p[i]<len(string)and string[i-p[i]]==string[i+p[i]]:
            p[i]+=1
        
        if mxBorder<p[i]+i:
            mxBorder=p[i]+i
            mxCenter=i
            if mxBorder-mxCenter>res[1]-res[0]:
                res=[mxCenter,mxBorder]
        
        i+=1
    
    return "".join([x for x in string[2*res[0]-res[1]+1:res[1]] if x!='#'])

#Test Cases
print question2('')
#

print question2('twotesttwo')
#tt

print question2('thrwowthr')
#wow

'''
Question 3
Given an undirected graph G, find the minimum spanning tree within G. A minimum spanning 
tree connects all vertices in a graph with the smallest possible total weight of edges. 
Your function should take in and return an adjacency list structured like this:
{'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)], 
 'C': [('B', 5)]}
Vertices are represented as unique strings. The function definition should be question3(G)
'''
# A utility function to find set of an element i
# (uses path compression technique)
def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

# A function that does union of two sets of x and y
# (uses union by rank)
def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    # Attach smaller rank tree under root of high rank tree
    # (Union by Rank)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    #If ranks are same, then make one as root and increment
    # its rank by one
    else :
        parent[yroot] = xroot
        rank[xroot] += 1

# The main function to construct MST using Kruskal's algorithm
def KruskalMST(graph, V, inv_dict):

    result =[] #This will store the resultant MST

    i = 0 # An index variable, used for sorted edges
    e = 0 # An index variable, used for result[]

    #Step 1:  Sort all the edges in non-decreasing order of their
    # weight.  If we are not allowed to change the given graph, we
    # can create a copy of graph
    graph =  sorted(graph,key=lambda item: item[2])

    parent = [] ; rank = []

    # Create V subsets with single elements
    for node in range(V):
        parent.append(node)
        rank.append(0)

    # Number of edges to be taken is equal to V-1
    while e < V -1 :

        # Step 2: Pick the smallest edge and increment the index
        # for next iteration
        u,v,w =  graph[i]
        i = i + 1
        x = find(parent, u)
        y = find(parent ,v)

        # If including this edge does't cause cycle, include it
        # in result and increment the index of result for next edge
        if x != y:
            e = e + 1
            result.append([u,v,w])
            union(parent, rank, x, y)
        # Else discard the edge

    # print the contents of result[] to display the built MST
    #print "Following are the edges in the constructed MST"
    p1 = []
    final_result = {}
    for u,v,weight  in result:
        p1 = [(inv_dict[v],weight)]
        if inv_dict[u] not in final_result:
            final_result[inv_dict[u]] = p1
        else:
            final_result[inv_dict[u]] = final_result[inv_dict[u]].append(p1)
        #print str(u) + " -- " + str(v) + " == " + str(weight)
        #print ("%c -- %c == %d" % (inv_dict[u],inv_dict[v],weight))

    return final_result

def question3(G):
    n = len(G)
    tmp_dict = {}
    inv_dict = {}
    count = 0
    u,v,w = None, None, None
    graph = []
    for i in G:
        tmp_dict[i] = count
        inv_dict[count] = i
        count += 1
    #print tmp_dict

    for i in G:
        for j in G[i]:
            #print tmp_dict[i], tmp_dict[j[0]], j[1]
            u,v,w = tmp_dict[i], tmp_dict[j[0]], j[1]
            graph.append([u,v,w])
    #print graph

    return KruskalMST(graph, count, inv_dict)

#Test Case
G = {'A': [('B', 2)],
          'B': [('A', 4), ('C', 2)],
          'C': [('A', 2), ('B', 5)]}
    print question3(G)	

#[[0, 2, 2], [1, 0, 2], [2, 1, 2], [2, 0, 4], [1, 2, 5]]
#{'A': [('B', 2)], 'C': [('A', 2)]}
	
'''
Question 4
Find the least common ancestor between two nodes on a binary search tree. The least common 
ancestor is the farthest node from the root that is an ancestor of both nodes. For example, 
the root is a common ancestor of all nodes on the tree, but if both nodes are descendents of 
the root's left child, then that left child might be the lowest common ancestor. You can assume 
that both nodes are in the tree, and the tree itself adheres to all BST properties. The function 
definition should look like question4(T, r, n1, n2), where Tis the tree represented as a matrix, 
where the index of the list is equal to the integer stored in that node and a 1 represents a child 
node, r is a non-negative integer representing the root, and n1 and n2 are non-negative integers 
representing the two nodes in no particular order. 
'''
class Node(object):
  def __init__(self, data):
    self.data = data
    self.right = None
    self.left = None

# Function to insert a new node at the beginning
def push_right(node, new_data):
    new_node = Node(new_data)
    node.right = new_node
    return new_node

# Function to insert a new node at the beginning
def push_left(node, new_data):
    new_node = Node(new_data)
    node.left = new_node
    return new_node

# Function to find LCA of n1 and n2. The function assumes
# that both n1 and n2 are present in BST
def leastCommonAncestor(head, n1, n2):
    # Base Case
    if head is None:
        return None

    # If both n1 and n2 are smaller than root, then LCA
    # lies in left
    if(head.data > n1 and head.data > n2):
        return leastCommonAncestor(head.left, n1, n2)

    # If both n1 and n2 are greater than root, then LCA
    # lies in right
    if(head.data < n1 and head.data < n2):
        return leastCommonAncestor(head.right, n1, n2)

    return head.data


def question4(T, r, n1, n2):
    global head
    # Make BST
    head = Node(r)
    head.left, head.right = None, None
    node_value = 0
    tmp_right, tmp_left = None, None
    node_list = []
    for elem in T[r]:
        if elem:
            if(node_value>r):
                node_list.append(push_right(head, node_value))
            else:
                node_list.append(push_left(head, node_value))
        node_value += 1

    tmp_node = node_list.pop(0)
    while tmp_node != None:
        node_value = 0
        for elem in T[tmp_node.data]:
            if elem:
                if(node_value>tmp_node.data):
                    node_list.append(push_right(tmp_node, node_value))
                else:
                    node_list.append(push_left(tmp_node, node_value))
            node_value += 1
        if node_list == []:
            break
        else:
            tmp_node = node_list.pop(0)

    return leastCommonAncestor(head, n1, n2)
	
#Test Case
print question4([[0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [1, 0, 0, 0, 1],
           [0, 0, 0, 0, 0]],
          3,
          1,
          2)
#1
	
'''
Question 5
Find the element in a singly linked list that's m elements from the end. For example, 
if a linked list has 5 elements, the 3rd element from the end is the 3rd element. 
The function definition should look like question5(ll, m), where ll is the first node 
of a linked list and m is the "mth number from the end". You should copy/paste the Node 
class below to use as a representation of a node in the linked list. 
Return the value of the node at that position.
'''
head = None

class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None

def push(new_data):
    global head
    new_node = Node(new_data)
    new_node.next = head
    head = new_node

def question5(ll, m):
    main_ptr = ll
    ref_ptr = ll
    count  = 0

    if(ll is not None):
        while(count < m ):
            if(ref_ptr is None):
                print "%d is greater than the no. of nodes in list" %(n)
                return

            ref_ptr = ref_ptr.next
            count += 1

    while(ref_ptr is not None):
        main_ptr = main_ptr.next
        ref_ptr = ref_ptr.next

    return main_ptr.data

#Test Case
global head
push(50)
push(40)
push(30)
push(20)
push(10)
print question5(head, 4)

#20