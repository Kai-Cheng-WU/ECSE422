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


# Can change signature
def get_sub_reliability(reliability_matrix, option):
    reliability = 1
    for i in range(len(reliability_matrix)):
        for j in range(len(reliability_matrix[i])):
            if option[i][j]:
                reliability *= reliability_matrix[i][j]

    return reliability


def part_of(subset, option, reliability_matrix):
    '''
    Returns (partOf, prob_of_missing edges)
    First tells us if it is a subset and then the probability of the missing edges so we can quickly multiply
    :param subset:
    :param option:
    :param reliability_matrix:
    :return:
    '''
    rel = 1
    for i in range(len(reliability_matrix)):
        for j in range(len(reliability_matrix[i])):
            if subset[i][j] == option[i][j]:  # If both are true or both false
                pass
            if subset[i][j] is True and option[i][j] is False:
                return False, 0
            if subset[i][j] is False and option[i][j] is True:
                rel *= (1 - reliability_matrix[i][j])
    if rel >= 1:
        raise Exception("Issue in PartOf")
    return True, rel


def get_graph(option):
    ### This function takes in an option and computes a graph from it
    ### The graph is essentially the option itself, but each edge is now bidirectional
    graph = copy.deepcopy(option)
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j]:
                graph[j][i] = True
    return graph


def get_valid(option):
    '''
    Returns if an option is valid ie possible have all-network reliability > 0
    :param option:
    :return:
    '''
    graph = get_graph(option)
    reached = set()
    discovered = queue.Queue()
    for i in range(len(graph)):
        if graph[0][i]:
            discovered.put(i)
            reached.add(0)

    while not discovered.empty():
        current = discovered.get()
        reached.add(current)
        for i in range(len(graph)):
            if graph[current][i] and i not in reached:
                discovered.put(i)
        if len(reached) == len(graph):
            return True, reached

    return False, reached

stringdic = {1: ['0', '1']}


def getStrings(n):
    if n in stringdic:
        return stringdic[n]
    if n == 0:
        return []
    if n == 1:
        return ['0', '1']
    to_ret = []
    for s in getStrings(n - 1):
        to_ret.append('0' + s)
        to_ret.append('1' + s)
    stringdic[n] = to_ret
    return to_ret


def getSituation(config, s):
    index = 0
    size = len(config)
    matr = [[None for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            if config[i][j]:
                matr[i][j] = s[index] == '1'
                index += 1
            else:
                matr[i][j] = False
    return matr


def get_prob(edges, s):
    p = 1
    for index, present in enumerate(s):
        if present == '1':
            p *= edges[index]
        else:
            p *= (1 - edges[index])
    return p


def getProbability(config, reliability_matrix):
    edges = []
    size = len(config)
    for i in range(size):
        for j in range(size):
            if config[i][j]:
                edges.append(reliability_matrix[i][j])
    p = 0
    # print(edges)
    for s in getStrings(len(edges)):
        situation = getSituation(config, s)
        if get_valid(situation)[0]:
            p += get_prob(edges, s)
    return p

def convert_to_matrix(edges,n):
    to_ret = [[None for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            to_ret[i][j] = False
    for edge in edges:
        i,j=edge
        to_ret[i][j] = True
    return to_ret

def get_cost_edges(edges, cost_matrix, n):
    return get_cost(convert_to_matrix(edges, n), cost_matrix)

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
