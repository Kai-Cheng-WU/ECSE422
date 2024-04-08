import sys

import helper
from helper import *


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


def augment(config, reliability_matrix, cost_matrix, cost_limit, number_cities):
    '''
    NOTE:The configuration is not passed as a matrix. For it to be in matrix, you can use the helper.convert_to_matrix()
    Example input: [(0, 3), (1, 3), (1, 2)]
    Takes the current configuration and the cost or reliability matrix and returns it with the next best edge added
    :param config: The configuration
    :param cr_matrix: cost or reliability matrix
    :return: new config
    '''

    config_init_matrix = helper.convert_to_matrix(config,number_cities)

    cost_now = get_cost_edges(config,cost_matrix,number_cities)
    print(cost_now)

    '''dict_remaining = {}

    for i in range(len(config_init_matrix)):
        for j in range(len(config_init_matrix[i])):
            if config_init_matrix[i][j] == False:
                dict_remaining.update({(i,j):(cost_matrix[i][j])})

    list_remaining = []
    for key in dict_remaining:
        list_remaining.append(dict_remaining[key])
        list_remaining.sort()
    print(list_remaining)
'''

    '''while sum of first i of list_remaining are less than cost_now:
            if i = 1 then
                go element by element and add to the actual config
                generate the probaility
                check the best
                
            increase i by 1    
            
            we will be back here.
            if i =2 then 
                go pair by pair an add to the actual config
                generate the probability
                check the best
            if i = 3 then
                go triple by triple which won't happen
    '''
    '''
    int_to_add = 1
    for i in range(1,len(list_remaining)):
        if sum(list_remaining[0:i]) < cost_now:
            int_to_add = i
    print("1Hello")
    print(dict_remaining)
    result = []
    for i in range(int_to_add):
        best_j = -1
        best_k = -1
        if i == 1:

            best_prob = 0.0


            for key in dict_remaining:
                dummy_config = []
                for element in config:
                    dummy_config.append(element)
                dummy_config.append((key))
                print("e")
                print(dummy_config)
                if get_cost_edges(dummy_config,cost_matrix,number_cities) < cost_limit:
                    probability = helper.getProbability(helper.convert_to_matrix(dummy_config, number_cities),reliability_matrix)
                    if probability > best_prob:
                        best_prob = probability
                        best_j = key[0]
                        best_k = key[1]

                '''

    best_reliability = 0.0
    best_j = -1
    best_k = -1
    for j in range(len(config_init_matrix)):
        for k in range(len(config_init_matrix[j])):
            # If an edge not added
            if config_init_matrix[j][k] == False:
                if cost_matrix[j][k] < (cost_limit - cost_now):
                    # Create dummy for reliability analysis
                    dummy_config = []
                    for element in config:
                        dummy_config.append(element)
                    dummy_config.append((j, k))
                    new_dummy_config = dummy_config
                    print(new_dummy_config)

                    current_best_reliability = (reliability_matrix[j][k]) * helper.getProbability(
                        helper.convert_to_matrix(new_dummy_config,number_cities), reliability_matrix) + (
                                                           1 - (reliability_matrix[j][k])) * helper.getProbability(
                        helper.convert_to_matrix(dummy_config,number_cities), reliability_matrix)
                    if current_best_reliability > best_reliability:
                        best_reliability = current_best_reliability
                        best_j = j
                        best_k = k

    if best_j != -1 and best_k != -1:
        config.append((best_j, best_k))
        print(config)
        print("bound")
        return config
    return config






    '''

    # Convert config to matrix for better analysis
    config_init_matrix = helper.convert_to_matrix(config,number_cities)


    #Reliability Analysis
    best_reliability = 0.0
    best_i = -1
    best_j = -1
    if not cost_approach:
        for i in range(len(config_init_matrix)):
            for j in range(len(config_init_matrix[i])):
                # If an edge not added
                if config_init_matrix[i][j] == False:
                    # Create dummy for reliability analysis
                    dummy_config = config
                    current_best_reliability = (reliability_matrix[i][j]) * helper.getProbability(dummy_config.append([i,j],reliability_matrix)) + (1 - (reliability_matrix[i][j])) * helper.getProbability(dummy_config,reliability_matrix)
                    if current_best_reliability > best_reliability and get_cost_edges(dummy_config,cost_matrix,num_of_cities) <= cost_limit:
                        best_reliability = current_best_reliability
                        best_i = i
                        best_j = j
        if best_i == -1 and best_j == -1:
            return config.append(config[0])
        else:
            return config.append((best_i,best_j))

    #cost analysis
    best_cost = 100
    best_i = -1
    best_j = -1
    if cost_approach:
        for i in range(len(config_init_matrix)):
            for j in range(len(config_init_matrix[i])):
                if config_init_matrix[i][j] == False:
                    dummy_config = config
                    current_cost = get_cost_edges(dummy_config.append((i,j)), cost_matrix,num_of_cities)
                    if current_cost <= cost_limit and current_cost <= best_cost:
                        best_cost = current_cost
                        best_i = i
                        best_j = j

        if best_i == -1 and best_j == -1:
            return config.append(config[0])

        else:
            print(best_i,best_j)
            return config.append((best_i, best_j))
'''










filename = '5_city.txt'
cost_limit = 60
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
print("mst_c")
print(cost_mst)
best_cost_config = augment(cost_mst,reliability_matrix,cost_matrix, cost_limit, num_of_cities)
'''cost_check = True
greedy_cost_with_cost_approach = get_cost_edges(best_cost_config, cost_matrix, num_of_cities)
while greedy_cost_with_cost_approach < cost_limit:
    #new_best_cost_config = augment(best_cost_config, cost_dictionary)
    new_best_cost_config = augment(best_cost_config,reliability_matrix,cost_matrix,cost_limit,num_of_cities,cost_check)
    new_cost = get_cost_edges(new_best_cost_config, cost_matrix, num_of_cities)
    if new_cost > cost_limit:
        break
    greedy_cost_with_cost_approach = new_cost
    best_cost_config = new_best_cost_config

'''

reliability_with_cost_approach = getProbability(convert_to_matrix(best_cost_config,num_of_cities), reliability_matrix)


# Get the best for reliability
# Make MST
reliability_dictionary = make_dict(reliability_matrix)
reliability_dictionary = order_dict(reliability_dictionary)
reliability_mst = primm_algo(reliability_dictionary)
print("mst_r")
print(reliability_mst)
best_reliability_config = augment(reliability_mst,reliability_matrix,cost_matrix, cost_limit, num_of_cities)
# continue until you add the max edges greedily according to cost
#cost_check = False
#greedy_cost_with_rel_approach = get_cost_edges(best_reliability_config, cost_matrix, num_of_cities)
#while greedy_cost_with_rel_approach < cost_limit:
#    # new_best_reliability_config = augment(best_reliability_config, reliability_dictionary)
#    new_best_reliability_config = augment(best_cost_config, reliability_matrix, cost_matrix, cost_limit, num_of_cities,
#                                         cost_check)
#    if new_cost > cost_limit:
#        break
#    greedy_cost_with_rel_approach = new_cost
#    best_reliability_config = new_best_reliability_config

reliability_with_reliability_approach = getProbability(convert_to_matrix(best_reliability_config,num_of_cities), reliability_matrix)

#if greedy_cost_with_rel_approach > cost_limit and greedy_cost_with_cost_approach > cost_limit:
#    print("No result")
#    exit()

if reliability_with_reliability_approach > reliability_with_cost_approach:
    print("Best Method: Reliability.")
    print(f'Best Reliability: {reliability_with_reliability_approach}')
    print("Best Cost: ", get_cost_edges(best_reliability_config,cost_matrix,num_of_cities))
    print_matrix(convert_to_matrix(best_reliability_config, num_of_cities), "-----")
else:
    print("Best Method: Cost.")
    print(f'Best Reliability: {reliability_with_cost_approach}')
    print("Best Cost: ", get_cost_edges(best_cost_config,cost_matrix,num_of_cities))
    print_matrix(convert_to_matrix(best_cost_config,num_of_cities), "-----")
