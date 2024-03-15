import sys

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


def print_matrix(matrix):
    '''
    prints an n x n matrix in an easy to read format
    :param matrix: input n x n matrix
    :return:
    '''
    for row in matrix:
        for el in row:
            line = el if el else '---'
            print(line, end=' ')
        print()


def bool_combinations(n):
    '''
    Returns n^2 combinations of booleans
    List is ordered from 11111 --> 11110 --> 11101 .... 00000
    :param n: size of boolean array
    :return: A list of list of booleans
    size of 'matrix' would be n x n
    '''
    if n == 1:
        return [[True], [False]]
    else:
        to_return = []
        for combination in bool_combinations(n - 1):
            m1 = []
            m1.extend(combination)
            m1.extend([True])
            m2 = []
            m2.extend(combination)
            m2.extend([False])
            to_return.append(m1)
            to_return.append(m2)
        return to_return


def add_line(bool_matrix_list, new_lines):
    if len(bool_matrix_list) == 0:
        return [[line] for line in new_lines]
    to_return = []
    for matrix in bool_matrix_list:
        for line in new_lines:
            new_matrix = matrix.copy()
            new_matrix.append(line)
            to_return.append(new_matrix)
    return to_return


# TODO
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


# TODO
# Can change signature
def get_enumerations(option):
    return []

# TODO
# Can change signature
def get_sub_reliability(enumeration, option):
    pass


def get_reliability(reliability_matrix, option):
    '''
    Returns the reliability of an option
    :param reliability_matrix:
    :param option:
    :return: reliability of an option
    '''
    reliability = 0
    enumerations = get_enumerations(option) # Can change signature or do another function for this
    for enumeration in enumerations:
        if get_valid(enumeration): # Can change signature or do another function for this
            reliability += get_sub_reliability(enumeration, option) # Can change signature or do another function for this
    return reliability

# TODO
def get_valid(option):
    '''
    Returns if an option is valid ie possible have all-network reliability > 0
    :param option:
    :return:
    '''
    return True

filename = '4_city.txt'
if len(sys.argv) > 2:
    print("Too many arguments.")
    exit(-1)
if len(sys.argv) == 2:
    filename = sys.argv[1]


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

# Listing all options
# Each option is a matrix of boolean to indicate which edge is included
options = []
for i in range(num_of_cities - 1, 0, -1):
    options = add_line(options, bool_combinations(i))
options = [make_square_matrix(option, num_of_cities) for option in options]
# print(len(options))

for option in options:
    cost = get_cost(cost_matrix, option)  # Get the cost of a design choice
    reliability = get_reliability(reliability_matrix, option)  # Get reliability of a design choice
    valid = get_valid(option)



