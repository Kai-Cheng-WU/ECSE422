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
    ''' reliability = 0
    enumerations = get_enumerations(option) # Can change signature or do another function for this
    for enumeration in enumerations:
        if get_valid(enumeration): # Can change signature or do another function for this
            reliability += get_sub_reliability(enumeration, option) # Can change signature or do another function for this
    return reliability
    '''

    '''New reliability done by Andrei. We multiply every reliabilities.'''
    reliability = 1
    for i in range(len(reliability_matrix)):
        for j in range(len(reliability_matrix[i])):
            if option[i][j]:
                reliability *= reliability_matrix[i][j]

    return reliability



# TODO
def get_valid(option):
    '''
    Returns if an option is valid ie possible have all-network reliability > 0
    :param option:
    :return:
    '''

    # Check if three true that connects everything, don't accept the triangle loop
    # accept the four true
    # accept the five true
    # accept the six true

def print_output(option):
    '''
    Returns the output of the best option
    :param option:
    :return: output
    '''
    if len(option[0]) == 4:
        print("The network looks like this")
        print(" (Node 1) o               o (Node 2)")
        print("")
        print("")
        print("")
        print(" (Node 3) o               o (Node 4)")

        if option[0][1]:
            print("There is a connection between node 1 and node 2")
        if option[0][2]:
            print("There is a connection between node 1 and node 3")
        if option[0][3]:
            print("There is a connection between node 1 and node 4")
        if option[1][2]:
            print("There is a connection between node 2 and node 3")
        if option[1][3]:
            print("There is a connection between node 2 and node 4")
        if option[2][3]:
            print("There is a connection between node 3 and node 4")

    if len(option[0]) == 5:
        print("The network looks like this")
        print(" (Node 1) o               o (Node 2)")
        print("")
        print("          (Node 5) o")
        print("")
        print(" (Node 3) o               o (Node 4)")

        if option[0][1]:
            print("There is a connection between node 1 and node 2")
        if option[0][2]:
            print("There is a connection between node 1 and node 3")
        if option[0][3]:
            print("There is a connection between node 1 and node 4")
        if option[0][4]:
            print("There is a connection between node 1 and node 5")
        if option[1][2]:
            print("There is a connection between node 2 and node 3")
        if option[1][3]:
            print("There is a connection between node 2 and node 4")
        if option[1][4]:
            print("There is a connection between node 2 and node 5")
        if option[2][3]:
            print("There is a connection between node 3 and node 4")
        if option[2][4]:
            print("There is a connection between node 3 and node 5")
        if option[3][4]:
            print("There is a connection between node 4 and node 5")

    if len(option[0]) == 6:
        print("The network looks like this")
        print("         (Node 1) o              ")
        print("      ")
        print(" (Node 2) o               o (Node 6)  ")
        print("")
        print(" (Node 3) o               o (Node 5)")
        print("      ")
        print("                  o (Node 4)")

        if option[0][1]:
            print("There is a connection between node 1 and node 2")
        if option[0][2]:
            print("There is a connection between node 1 and node 3")
        if option[0][3]:
            print("There is a connection between node 1 and node 4")
        if option[0][4]:
            print("There is a connection between node 1 and node 5")
        if option[0][5]:
            print("There is a connection between node 1 and node 6")

        if option[1][2]:
            print("There is a connection between node 2 and node 3")
        if option[1][3]:
            print("There is a connection between node 2 and node 4")
        if option[1][4]:
            print("There is a connection between node 2 and node 5")
        if option[1][5]:
            print("There is a connection between node 2 and node 6")

        if option[2][3]:
            print("There is a connection between node 3 and node 4")
        if option[2][4]:
            print("There is a connection between node 3 and node 5")
        if option[2][5]:
            print("There is a connection between node 3 and node 6")

        if option[3][4]:
            print("There is a connection between node 4 and node 5")
        if option[3][5]:
            print("There is a connection between node 4 and node 6")

        if option[4][5]:
            print("There is a connection between node 5 and node 6")




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

option5 = [[True,False,False,False,False,True],[True,False,False,False,False,True],[True,False,False,False,False,True],[True,False,False,False,False,True],[True,False,False,False,False,True]]
print_matrix(options[1])
print_output(option5)

