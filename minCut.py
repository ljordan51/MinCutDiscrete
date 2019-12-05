import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

"""
Notes:
Think about how to handle multiple nodes connected together (nets between more than two nodes)
    maybe look for euler/hamilton paths circuits first
"""

E = [
    ["N1", "N2", 1],
    ["N2", "N4", 1],
    ["N4", "N5", 1],
    ["N3", "N12", 1],
    ["N6", "N15", 1],
    ["N101", "N201", 1],
    ["N102", "N202", 1],
    ["N103", "N203", 1],
    ["N104", "N204", 1],
    ["N105", "N205", 1],
    ["N106", "N206", 1],
    ["N107", "N207", 1],
    ["N108", "N208", 1],
    ["N1", "N101", 1],
    ["N1", "N202", 1],
    ["N105", "N2", 1],
    ["N103", "N4", 1],
    ["N109", "N5", 1],
    ["N1", "N12", 1],
    ["N101", "N15", 1],
    ["N101", "N205", 1],
    ["N102", "N208", 1],
    ["N103", "N207", 1],
    ["N104", "N206", 1],
    ["N105", "N101", 1],
    ["N106", "N109", 1],
    ["N107", "N102", 1],
    ["N108", "N107", 1],
    ["N109", "N208", 1]
]

def createNxGraph(edge_list):
    G = nx.Graph()
    edge_tuples = [(edge[0], edge[1]) for edge in edge_list]
    G.add_edges_from(edge_tuples)
    return G
    

def createPosFromNestedNodeList(node_list, num_nodes, orientation=True, center=[0,0], step=0):
    res = {}
    spacing = [0.4, 0.4, 0.2, 0.2]
    
    if (node_list[-1]=="end"):
        for i in range(len(node_list)-1):
            if orientation:
                res[node_list[i]] = np.array([center[0]+i*0.2-0.1, center[1]])
            else:
                res[node_list[i]] = np.array([center[0], center[1]+i*0.2-0.1])
    else:
        if orientation:
            d1 = createPosFromNestedNodeList(node_list[0], num_nodes, False, [center[0]+spacing[step], center[1]], step+1)
            d2 = createPosFromNestedNodeList(node_list[1], num_nodes, False, [center[0]-spacing[step], center[1]], step+1)
            d1.update(d2)
            res = d1
        else:
            d1 = createPosFromNestedNodeList(node_list[0], num_nodes, True, [center[0], center[1]+spacing[step]], step+1)
            d2 = createPosFromNestedNodeList(node_list[1], num_nodes, True, [center[0], center[1]-spacing[step]], step+1)
            d1.update(d2)
            res = d1
    return res


def drawGraph(graph, nested_node_list):
    # pos = nx.circular_layout(graph)
    pos = createPosFromNestedNodeList(nested_node_list, len(graph.nodes))
    print("Pos: ")
    print(pos)
    # values = [colors.get(node, 'blue') for node in graph.nodes()]
    # nx.draw(graph, pos, with_labels = False, node_color=values, edge_color='black', width=1, alpha=0.7)
    nx.draw(graph, pos=pos, with_labels=True, edge_color='black', width=1, alpha=0.7)


def createNodeDict(edge_list):
    dict = {}
    for edge in edge_list:
        dict[edge[0]] = edge[0]
        dict[edge[1]] = edge[1]
    return dict


def randomSplit(nodes):
    keys = list(nodes.keys()) # because nodes is a dict
    random.shuffle(keys) # this can be better in terms of time complexity later
    partition_size = math.floor(len(keys)/2)
    partition1 = keys[:partition_size] if (len(keys) % 2 == 0) else keys[:partition_size+1]
    partition2 = keys[len(keys)-partition_size:]
    return (dict(zip(partition1, partition1)), dict(zip(partition2, partition2)))


def getCutWeight(edge_list, node_dict_1, node_dict_2):
    cut_weight = 0
    for edge in edge_list:
        node1, node2, weight = edge
        if (node_dict_1.get(node1) and node_dict_2.get(node2)):
            cut_weight += weight
        elif (node_dict_1.get(node2) and node_dict_2.get(node1)):
            cut_weight += weight
    return cut_weight


def randomProb():
    probability = .05
    range_size = math.ceil(1/probability)
    rand_int = random.randint(1, range_size)
    return (rand_int == range_size)


def minCutAlgo(edge_list, node_dict):
    # handle recursive base case
    if (len(node_dict) <= 2):
        return list(node_dict.keys()) + ["end"]

    node_dict_1, node_dict_2 = randomSplit(node_dict) # randomly separate into two groups

    # get cut weight
    best_cut_weight = getCutWeight(edge_list, node_dict_1, node_dict_2)
    # print("Initial cut weight: " + str(best_cut_weight))
    swapped = True

    while(swapped):
        # check initial cut cut_weight
        if (best_cut_weight == 0):
            swapped=False
            res = [minCutAlgo(edge_list, node_dict_1), minCutAlgo(edge_list,node_dict_2)]
            break
        
        # pick random nodes
        node1 = node_dict_1.pop(random.choice(list(node_dict_1.keys())))
        node2 = node_dict_2.pop(random.choice(list(node_dict_2.keys())))

        # swap them
        node_dict_1[node2] = node2
        node_dict_2[node1] = node1

        # evaluate cut weight
        cut_weight = getCutWeight(edge_list, node_dict_1, node_dict_2)

        # compare, swap with probability (if worse)
        if (cut_weight == 0):
            best_cut_weight = cut_weight
            swapped = False
            res = [minCutAlgo(edge_list, node_dict_1), minCutAlgo(edge_list,node_dict_2)]
        elif (cut_weight < best_cut_weight):
            best_cut_weight = cut_weight
        elif (~randomProb()):
            swapped = False
            node_dict_1.pop(node2)
            node_dict_2.pop(node1)
            node_dict_1[node1] = node1
            node_dict_2[node2] = node2
            res = [minCutAlgo(edge_list, node_dict_1), minCutAlgo(edge_list,node_dict_2)]

    print("Best cut weight: " + str(best_cut_weight))
    print(res)

    return res

nested_node_list = minCutAlgo(E, createNodeDict(E))
print(nested_node_list)
G = createNxGraph(E)
drawGraph(G, nested_node_list)
plt.show()
