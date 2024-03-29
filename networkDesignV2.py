import sys
from helper import *


def make_dict(cr_matrix):
    # output as dictionary
    result_dictionary = {}
    for i in range(len(cr_matrix)):
        for j in range(len(cr_matrix[i])):
            if cr_matrix[i][j]:
                result_dictionary.update({(i, j): cr_matrix[i][j]})

    return result_dictionary


def order_dict(cr_dict, rev=False):
    cr_dict = sorted(cr_dict.items(), key=lambda x: x[1], reverse=rev)
    sortdict = dict(cr_dict)
    # print(sortdict)
    return sortdict


def primm_algo(matrix):
    '''
    input: the cost or reliability matrix
    :return: MST
    '''
    target = num_of_cities
    present = []
    added = []
    unadded = []
    for edge, _ in matrix.items():
        if len(present) == target:
            return added
        a, b = edge
        if len(present) == 0:  # Add the first edge
            present.append(a)
            present.append(b)
            added.append(edge)
            continue
        if a in present and b in present:
            continue
        if a in present and b not in present:
            present.append(b)
            added.append(edge)
            continue
        if a not in present and b in present:
            present.append(a)
            added.append(edge)
            continue
        # If neither present
        for uedge in unadded:
            x, y = uedge
            if x in present and y not in present:
                present.append(y)
                added.append(uedge)
                unadded.remove(uedge)
                continue
            if x not in present and y in present:
                present.append(x)
                added.append(edge)
                added.append(uedge)
                unadded.remove(uedge)
                continue
        unadded.append(edge)
    return added


def augment(config, cr_matrix):
    '''
    :param config:
    :param cr_matrix: cost or reliability matrix
    :return: new config
    '''
    pass


filename = '4_city.txt'
cost_limit = 85
verbose = False
if len(sys.argv) > 4:
    print("Too many arguments.")
    exit(-1)
if len(sys.argv) > 1:  # First argument is filename
    filename = sys.argv[1]
if len(sys.argv) > 2:  # Second argument is cost limit
    cost_limit = int(sys.argv[2])
if len(sys.argv) > 3:  # Third argument is verbose
    verbose = sys.argv[3] == "True"

# Input variables
num_of_cities = 0
reliability_matrix = []
cost_matrix = []

# READ FILE
# Assume file is always formatted correctly
print(f"Reading {filename}.\n")
with open(filename, 'r') as f:
    num_of_cities = int(get_next_line(f))

    # Get reliability matrix
    # Get next valid (num_of_cities -1) lines
    # Then put them into an array of floats
    for i in range(num_of_cities - 1):
        line = get_next_line(f)
        line = line.split()
        line = [float(i) for i in line]
        reliability_matrix.append(line)

    # Get cost matrix
    # Get next valid (num_of_cities -1) lines
    # Then put them into an array of ints
    for i in range(num_of_cities - 1):
        line = get_next_line(f)
        line = line.split()
        line = [int(i) for i in line]
        cost_matrix.append(line)

# Convert matrices into square_matrices
reliability_matrix = make_square_matrix(reliability_matrix, num_of_cities)
cost_matrix = make_square_matrix(cost_matrix, num_of_cities)

# Print the values to check correctness
print(f"Number of cities: {num_of_cities}")
print("Reliability Matrix: \n")
print_matrix(reliability_matrix)
print("Cost Matrix: \n")
print_matrix(cost_matrix)

# Get the best for cost
# Make the MST
cost_dictionary = make_dict(cost_matrix)
cost_dictionary = order_dict(cost_dictionary)
cost_mst = primm_algo(cost_dictionary)
print(cost_mst)

best_cost_config = cost_mst
# continue until you add the max edges greedily according to cost
greedy_cost_with_cost_approach = get_cost_edges(best_cost_config)
while greedy_cost_with_cost_approach < cost_limit:
    best_cost_config = augment(best_cost_config, cost_dictionary)
    new_cost = get_cost_edges(best_cost_config, cost_matrix, num_of_cities)
    if new_cost > cost_limit:
        break
    greedy_cost_with_cost_approach = new_cost
reliability_with_cost_approach = getProbability(best_cost_config, reliability_matrix)

# Get the best for reliability
# Make MST
reliability_dictionary = make_dict(reliability_matrix)
reliability_dictionary = order_dict(reliability_dictionary)
reliability_mst = primm_algo(reliability_dictionary)
best_reliability_config = reliability_mst
# continue until you add the max edges greedily according to cost
greedy_cost_with_rel_approach = get_cost_edges(best_reliability_config)
while greedy_cost_with_rel_approach < cost_limit:
    best_reliability_config = augment(best_reliability_config, reliability_dictionary)
    new_cost = get_cost_edges(best_reliability_config, cost_matrix, num_of_cities)
    if new_cost > cost_limit:
        break
    greedy_cost_with_rel_approach = new_cost
reliability_with_reliability_approach = getProbability(best_reliability_config, reliability_matrix)

if greedy_cost_with_rel_approach > cost_limit and greedy_cost_with_cost_approach > cost_limit:
    print("No result")
    exit()

if reliability_with_reliability_approach > reliability_with_cost_approach:
    print(f'Best Reliability: {reliability_with_reliability_approach}')
    print("Best Cost: ", greedy_cost_with_rel_approach)
    print_matrix(best_reliability_config, "-----")
else:
    print(f'Best Reliability: {reliability_with_cost_approach}')
    print("Best Cost: ", greedy_cost_with_cost_approach)
    print_matrix(best_cost_config, "-----")
