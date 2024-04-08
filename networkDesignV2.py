import sys
from helper import *
import time

t1 = time.time()

def make_dict(cr_matrix):
    '''
    Takes a cost or reliability matrix and turns it into a dictionary.
    The keys are the edges as vertices pairs and the cost or reliability as values
    :param cr_matrix: Cost or reliability matrix
    :return: dictionary representation of the matrix
    '''
    # output as dictionary
    result_dictionary = {}
    for i in range(len(cr_matrix)):
        for j in range(len(cr_matrix[i])):
            if cr_matrix[i][j]:
                result_dictionary.update({(i, j): cr_matrix[i][j]})

    return result_dictionary


def order_dict(cr_dict, rev=False):
    '''
    Orders the dictionary
    :param cr_dict: cost or reliability matrix
    :param rev: if True, descending order, if False, ascending order
    :return: The dictionary ordered according to the costs or reliability
    '''
    cr_dict = sorted(cr_dict.items(), key=lambda x: x[1], reverse=rev)
    sortdict = dict(cr_dict)
    # print(sortdict)
    return sortdict

def order_dict_rel_per_cost(rel_dict, cost_dict):

    # Calculate reliability per cost
    reliability_per_cost = {item: rel_dict[item] / cost_dict[item] for item in cost_dict}

    # Sort rel_dict by reliability per cost ratio
    sortdict = {k: v for k, v in sorted(rel_dict.items(), key=lambda item: reliability_per_cost[item[0]], reverse=True)}

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


def augment_cost(config, c_dict):
    '''
    NOTE:The configuration is not passed as a matrix. For it to be in matrix, you can use the helper.convert_to_matrix()
    Example input: [(0, 3), (1, 3), (1, 2)]
    Takes the current configuration and the cost matrix and returns it with the next best edge added
    :param config: The configuration
    :param c_matrix: cost matrix
    :return: new config
    '''
    config_set = set(config)
    for edge, cost in c_dict.items():
        if edge not in config_set:
            new_config = copy.deepcopy(config)
            new_config.append(edge)
            return new_config

def augment_reliability(config, r_dict, cost_limit):
    '''
    NOTE:The configuration is not passed as a matrix. For it to be in matrix, you can use the helper.convert_to_matrix()
    Example input: [(0, 3), (1, 3), (1, 2)]
    Takes the current configuration and the reliability matrix and returns it with the next best edge added
    :param config: The configuration
    :param r_matrix: reliability matrix
    :return: new config
    '''
    config_set = set(config)
    candidates = []
    for edge, cost in r_dict.items():
        if edge not in config_set:
            candidate = copy.deepcopy(config)
            candidate.append(edge)
            candidates.append(candidate)

    if candidates.count == 0:
        return config
    
    best_candidate = candidates[0]
    for curr in candidates:
        # print(f"Config: {config}")
        # print(f"Current: {curr}")
        if getProbability(convert_to_matrix(curr, num_of_cities), reliability_matrix) > getProbability(convert_to_matrix(best_candidate, num_of_cities), reliability_matrix) and get_cost_edges(curr, cost_matrix, num_of_cities) <= cost_limit:
            best_candidate = curr
    return best_candidate


def augment_reliability_per_cost(config, r_dict, c_dict, cost_limit):
    '''
    NOTE:The configuration is not passed as a matrix. For it to be in matrix, you can use the helper.convert_to_matrix()
    Example input: [(0, 3), (1, 3), (1, 2)]
    Takes the current configuration and the reliability matrix and returns it with the next best edge added
    :param config: The configuration
    :param r_matrix: reliability matrix
    :return: new config
    '''
    config_set = set(config)
    candidates = []
    for edge, cost in r_dict.items():
        if edge not in config_set:
            candidate = copy.deepcopy(config)
            candidate.append(edge)
            candidates.append(candidate)

    if candidates.count == 0:
        return config
    
    best_candidate = candidates[0]
    for curr in candidates:
        # print(f"Config: {config}")
        # print(f"Current: {curr}")
        currprob = getProbability(convert_to_matrix(curr, num_of_cities), reliability_matrix)
        currcost = get_cost_edges(curr, cost_matrix, num_of_cities) 
        prevprob = getProbability(convert_to_matrix(best_candidate, num_of_cities), reliability_matrix)
        prevcost = get_cost_edges(best_candidate, cost_matrix, num_of_cities)
        if currprob / currcost > prevprob / prevcost and get_cost_edges(curr, cost_matrix, num_of_cities) <= cost_limit:
            best_candidate = curr
    return best_candidate



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
print("Method: MST and Augmentation")

# Get the best for cost
# Make the MST
cost_dictionary = make_dict(cost_matrix)
cost_dictionary = order_dict(cost_dictionary, False)
cost_mst = primm_algo(cost_dictionary)
best_cost_config = cost_mst
# continue until you add the max edges greedily according to cost
greedy_cost_with_cost_approach = get_cost_edges(best_cost_config, cost_matrix, num_of_cities)
while greedy_cost_with_cost_approach < cost_limit:
    new_best_cost_config = augment_cost(best_cost_config, cost_dictionary)
    new_cost = get_cost_edges(new_best_cost_config, cost_matrix, num_of_cities)
    if new_cost > cost_limit:
        break
    greedy_cost_with_cost_approach = new_cost
    best_cost_config = new_best_cost_config
reliability_with_cost_approach = getProbability(convert_to_matrix(best_cost_config,num_of_cities), reliability_matrix)

# Get the best for reliability
# Make MST
reliability_dictionary = make_dict(reliability_matrix)
reliability_dictionary = order_dict(reliability_dictionary, True)
reliability_mst = primm_algo(reliability_dictionary)
best_reliability_config = reliability_mst
# continue until you add the max edges greedily according to cost
greedy_cost_with_rel_approach = get_cost_edges(best_reliability_config, cost_matrix, num_of_cities)
while greedy_cost_with_rel_approach < cost_limit:
    new_best_reliability_config = augment_reliability(best_reliability_config, reliability_dictionary, cost_limit)
    new_cost = get_cost_edges(new_best_reliability_config, cost_matrix, num_of_cities)
    if new_cost > cost_limit:
        break
    greedy_cost_with_rel_approach = new_cost
    best_reliability_config = new_best_reliability_config
reliability_with_reliability_approach = getProbability(convert_to_matrix(best_reliability_config,num_of_cities), reliability_matrix)

# Get the best for rel/cost
# Make MST
reliability_dictionary = make_dict(reliability_matrix)
reliability_dictionary = order_dict_rel_per_cost(reliability_dictionary, cost_dictionary)
reliability_mst = primm_algo(reliability_dictionary)
best_cr_config = reliability_mst
# continue until you add the max edges greedily according to cost
greedy_cost_with_rel_approach = get_cost_edges(best_reliability_config, cost_matrix, num_of_cities)
while greedy_cost_with_rel_approach <= cost_limit:
    new_best_reliability_config = augment_reliability_per_cost(best_reliability_config, reliability_dictionary, cost_dictionary, cost_limit)
    new_cost = get_cost_edges(new_best_reliability_config, cost_matrix, num_of_cities)
    if new_cost > cost_limit:
        break
    greedy_cost_with_rel_approach = new_cost
    best_reliability_config = new_best_reliability_config
reliability_with_cr_approach = getProbability(convert_to_matrix(best_reliability_config,num_of_cities), reliability_matrix)



if greedy_cost_with_rel_approach > cost_limit and greedy_cost_with_cost_approach > cost_limit and greedy_cost_with_rel_approach > cost_limit:
    print("INFEASIBLE: Cost goal is infeasible")
    exit()

best = max(reliability_with_reliability_approach, reliability_with_cost_approach, reliability_with_cr_approach)

if best == reliability_with_reliability_approach:
    print("Best Method: Reliability.")
    print(f'Best Reliability: {reliability_with_reliability_approach}')
    print("Best Cost: ", greedy_cost_with_rel_approach)
    print_matrix(convert_to_matrix(best_reliability_config, num_of_cities), "-----")
elif best == reliability_with_cost_approach:
    print("Best Method: Cost.")
    print(f'Best Reliability: {reliability_with_cost_approach}')
    print("Best Cost: ", greedy_cost_with_cost_approach)
    print_matrix(convert_to_matrix(best_cost_config,num_of_cities), "-----")
else:
    print("Best Method: Reliability/Cost.")
    print(f'Best Reliability: {reliability_with_cr_approach}')
    print("Best Cost: ", greedy_cost_with_rel_approach)
    print_matrix(convert_to_matrix(best_cr_config, num_of_cities), "-----")

print(f'time taken: {(time.time() - t1)}')