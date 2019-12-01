import random
import math

"""
Notes:
Think about how to handle multiple nodes connected together (nets between more than two nodes)
    maybe look for euler/hamilton paths circuits first
"""

E = [
    ["N1", "N2", 1],
    ["N2", "N4", 1],
    ["N4", "N5", 1],
    ["N3", "N12", 10],
    ["N6", "N15", 10],
    ["N101", "N201", 1],
    ["N102", "N202", 1],
    ["N103", "N203", 1],
    ["N104", "N204", 1],
    ["N105", "N205", 1],
    ["N106", "N206", 1],
    ["N107", "N207", 1],
    ["N108", "N208", 1],
    ["N109", "N205", 1]
]

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
    probability = .1
    range_size = math.ceil(1/probability)
    rand_int = random.randint(1, range_size)
    print(range_size)
    print(rand_int)
    print(rand_int/range_size)
    return (rand_int/range_size >= 0.5)


def minCutAlgo(edge_list, node_dict):
    # handle recursive base case

    node_dict_1, node_dict_2 = randomSplit(node_dict)# randomly separate into two groups
    print(node_dict_1)
    print(node_dict_2)

    # get cut weight
    best_cut_weight = getCutWeight(edge_list, node_dict_1, node_dict_2)
    print(best_cut_weight)
    swapped = True

    while(swapped):
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
        elif (cut_weight < best_cut_weight):
            best_cut_weight = cut_weight
        elif (randomProb()):
            best_cut_weight = cut_weight
        else:
            swapped = False
            node_dict_1.pop(node2)
            node_dict_2.pop(node1)
            node_dict_1[node1] = node1
            node_dict_2[node2] = node2
            res = [minCutAlgo(edge_list, node_dict_1), minCutAlgo(edge_list,node_dict_2)]

        print(best_cut_weight)

    return res


print(minCutAlgo(E, createNodeDict(E)))
