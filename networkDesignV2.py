import sys
import queue
import copy

def get_next_line(f):
    '''
    Gets the next line in the file that is not a comment
    :param f: File descriptor object
    :return: type(str) next line in the
    '''
    line = f.readline()
    while line[0] == '#':
        line = f.readline()
    return line


def make_square_matrix(matrix1, size):
    '''
    Transforms an incomplete matrix into a square matrix
    eg [1,1,1], [1,1], [1]  --> [-,1,1,1], [-,-,1,1], [-,-,-,1], [-,-,-,-]
    :param matrix1: The input incomplete matrix
    :param size: size of the final matrix/ the number of cities
    :return: n x n matrix that has the same information as the the input matrix
    only half (triangular part) of the matrix is filled in
    '''
    matrix1.append([])
    for i in range(size):
        line = [None for x in range(i + 1)]
        line.extend(matrix1[i])
        matrix1[i] = line
    return matrix1


def print_matrix(matrix, filler='---'):
    '''
    prints an n x n matrix in an easy to read format
    :param matrix: input n x n matrix
    :return:
    '''
    for row in matrix:
        for el in row:
            line = el if el is not None else filler
            print(line, end=' ')
        print()

def make_dict(cr_matrix):
    # output as dictionary
    result_dictionary = {}
    for i in range(len(cr_matrix)):
        for j in range(len(cr_matrix[i])):
            if cr_matrix[i][j]:
                result_dictionary.update({(i+1,j+1) : cr_matrix[i][j]})

    return result_dictionary

def order_dict(cr_dict):
    cr_dict = sorted(cr_dict.items(), key=lambda x: x[1])
    sortdict = dict(cr_dict)
    print(sortdict)

def primm_algo(matrix):
    '''
    input: the cost or reliability matrix
    :return: MST
    '''

def detect_loop(config):
    '''
    :param config:
    :return:
    '''
    pass

def augment(config, cr_matrix):
    '''
    :param config:
    :param cr_matrix: cost or reliability matrix
    :return: new config
    '''
    pass

def get_cost(cost_matrix, option):
    '''
    Returns the cost of a design option
    :param cost_matrix:
    :param option:
    :return: the cost as an int
    '''
    cost_option = 0
    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[i])):
            if option[i][j]:
                cost_option += cost_matrix[i][j]

    return cost_option

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

dict1 = make_dict(cost_matrix)
print(dict1)
ordered = order_dict(dict1)
print(ordered)
#make_dict(reliability_matrix)
#order_matrix()