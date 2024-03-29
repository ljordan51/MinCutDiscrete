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

MIN_RUNS = 5000

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
    ["N1", "N20", 1],
    ["N2", "N40", 1],
    ["N4", "N50", 1],
    ["N3", "N120", 1],
    ["N6", "N150", 1],
    ["N101", "N2010", 1],
    ["N102", "N2020", 1],
    ["N103", "N2030", 1],
    ["N104", "N2040", 1],
    ["N105", "N2050", 1],
    ["N106", "N2060", 1],
    ["N107", "N2070", 1],
    ["N108", "N2080", 1],
    ["N1", "N1010", 1],
    ["N1", "N2020", 1],
    ["N105", "N20", 1],
    ["N103", "N40", 1],
    ["N109", "N50", 1],
    ["N1", "N120", 1],
    ["N101", "N150", 1],
    ["N101", "N2050", 1],
    ["N102", "N2080", 1],
    ["N103", "N2070", 1],
    ["N104", "N2060", 1],
    ["N105", "N1010", 1],
    ["N106", "N1090", 1],
    ["N107", "N1020", 1],
    ["N108", "N1070", 1],
    ["N109", "N2080", 1]
]

def createNxGraph(edge_list):
    G = nx.Graph()
    edge_tuples = [(edge[0], edge[1]) for edge in edge_list]
    G.add_edges_from(edge_tuples)
    return G
    

def createPosFromNestedNodeList(node_list, num_nodes, orientation=True, center=[0,0], step=0):
    res = {}
    depth = math.ceil(math.log(num_nodes, 2))
    spacing = []
    for i in range(depth):
        padding = (2**math.floor(i/2))*0.2
        spacing = [padding] + spacing
    
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
    pos = createPosFromNestedNodeList(nested_node_list, len(graph.nodes))
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
    best_dicts = [node_dict_1, node_dict_2]
    runs = 0

    while(runs<MIN_RUNS):
        runs+=1
        # check initial cut cut_weight
        if (best_cut_weight == 0):
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
        if (cut_weight < best_cut_weight):
            best_cut_weight = cut_weight
            best_dicts = [node_dict_1, node_dict_2]
        elif (~randomProb()):
            node_dict_1.pop(node2)
            node_dict_2.pop(node1)
            node_dict_1[node1] = node1
            node_dict_2[node2] = node2

    res = [minCutAlgo(edge_list, best_dicts[0]), minCutAlgo(edge_list, best_dicts[1])]

    # print("Best cut weight: " + str(best_cut_weight))
    return res


node_dict = createNodeDict(E)
print(len(node_dict))
nested_node_list = minCutAlgo(E, node_dict)
G = createNxGraph(E)
drawGraph(G, nested_node_list)
plt.show()
