import sys
from helper import *

def make_dict(cr_matrix):
    # output as dictionary
    result_dictionary = {}
    for i in range(len(cr_matrix)):
        for j in range(len(cr_matrix[i])):
            if cr_matrix[i][j]:
                result_dictionary.update({(i+1,j+1) : cr_matrix[i][j]})

    return result_dictionary

def order_dict(cr_dict,rev=False):
    cr_dict = sorted(cr_dict.items(), key=lambda x: x[1],reverse=rev)
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
        if len(present) == 0: # Add the first edge
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

cost_dict = make_dict(cost_matrix)
cost_dict = order_dict(cost_dict)
print(cost_dict)
print(primm_algo(cost_dict))


reliability_dict = make_dict(reliability_matrix)
reliability_dict = order_dict(reliability_dict)
print(reliability_dict)
print(primm_algo(reliability_dict))