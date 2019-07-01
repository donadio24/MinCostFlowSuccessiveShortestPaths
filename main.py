import sys
import Graphic as g
import random

from Graph import Graph
from Elements import Node
from Elements import Edge


def createGraph():
    dim = 6
    nodes = random.randint(4,dim)

    bound = round(nodes/3,0)

    overflow = random.randint(2, bound)
    defect = random.randint(2, bound)

    graph = Graph()
    balance = 0
    value = 1
    transitNodes = nodes - overflow - defect

    for i in range(defect):
        b = random.randint(1,10)
        graph.addNode(Node(value, -b, {}))
        value += 1
        balance += b

    for i in range(transitNodes):
        graph.addNode(Node(value, 0, {}))
        value += 1


    for i in range(overflow):
        b = random.randint(1,10)
        if balance - b < 0:
            graph.addNode(Node(value, balance, {}))
            value += 1
            break

        graph.addNode(Node(value,b,{}))
        value += 1
        balance -= b



    for node in graph.nodes:
        numEdges = random.randint(1,4)
        for i in range(numEdges):
            edge = random.randint(1,len(graph.nodes))
            #if edge >= len(graph.nodes):
             #   continue
            weight = random.randint(1,15)
            capacity = random.randint(1,15)

            node.addEdge(Edge(graph.nodes[edge-1],capacity,weight))

    return graph


# node(value,balance, { exitEdges(node,capacity,weight})

node6 = Node(6,-2, {})
node5 = Node(5,0, {6: Edge(node6,2,2)})
node4 = Node(4,-2, {5: Edge(node5,1,2), 6: Edge(node6,1,2)})
node2 = Node(2,0, {4: Edge(node4,6,5)})
node3 = Node(3,1, {2: Edge(node2,2,1), 4: Edge(node4,5,2), 5: Edge(node5,2,2)})
node1 = Node(1,3, {2: Edge(node2,4,2), 3: Edge(node3,1,3)})
nodes = [node1,node2,node3,node4,node5,node6]

'''
node6 = Node(6,-5, {})
node5 = Node(5,-2, {6: Edge(node6,9,3)})
node2 = Node(2,0, {5: Edge(node5,5,1)})
node3 = Node(3,0, {2: Edge(node2,5,4), 6: Edge(node6,5,2)})
node4 = Node(4,0, {6: Edge(node6,7,2), 3: Edge(node3,2,5)})
node1 = Node(1,7, {2: Edge(node2,6,2), 3: Edge(node3,7,3), 4: Edge(node4,5,1)})
nodes = [node1,node2,node3,node4,node5,node6]
'''
'''
node4 = Node(4,-4, {})
node3 = Node(3,0, {4: Edge(node4,5,1)})
node2 = Node(2,0, {3: Edge(node3,2,1), 4: Edge(node4,3,3)})
node1 = Node(1,4, {2: Edge(node2,4,2), 3: Edge(node3,2,2)})
nodes = [node1,node2,node3,node4]
'''
defectsNode = []
overflowNode = []

#graph = Graph(nodes)

graph = createGraph()

# create overflowNodes and defectNodes list
for node in graph.nodes:
    if node.balance > 0:
        overflowNode.append(node.value)
    elif node.balance < 0:
        defectsNode.append(node.value)

print("nodes = %d" %len(graph.nodes))
print("overflow = " + str(overflowNode))
print("defect = " + str(defectsNode)+ "\n")
iteration = 0
g.drawResidualGraph(graph,iteration)
iteration += 1

while len(overflowNode) > 0 and len(defectsNode) > 0:
    path = graph.findPath(overflowNode, defectsNode)
  #  print(path)

    # check if there is no path from overflowNodes to defectNodes
    if path == []:
        break

    # find minimum residual capacity in path
    minim = sys.maxsize
    for i in range(len(path)-1):
        residual = graph.nodes[path[i] - 1].edges[path[i+1]].residualCapacity
        if residual < minim:
            minim = residual

    # find minimum flow that can be sent in the path
    flow = min(abs(graph.nodes[path[0]-1].balance), abs(graph.nodes[path[-1]-1].balance), minim)
    #print(flow)

    # increase flow and update reduct costs in edges of the path
    graph.updateCosts()
    graph.updateFlow(flow, path)

    # update balances of root and end node in path
    graph.updateBalance(path[0], path[-1], flow)

    # check if root node can exit from overflowNode
    if graph.nodes[path[0]-1].balance == 0:
        overflowNode.remove(path[0])

    # check if end node can exit from defectNode
    if graph.nodes[path[-1]-1].balance == 0:
        defectsNode.remove(path[-1])

    #print(overflowNode)
    #print(defectsNode)

    g.drawResidualGraph(graph,iteration)
    iteration += 1
    graph.print()

g.drawGraph(graph)