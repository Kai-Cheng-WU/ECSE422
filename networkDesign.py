import sys
from helper import *
import time

t1 = time.time()


def get_reliability(reliability_matrix, option, subsets):
    '''
    Returns the reliability of an option
    :param reliability_matrix:
    :param option:
    :param subsets: list of tuples with options and probability
    :return: reliability of an option
    '''
    valid, nodes = get_valid(option)
    if not valid:
        return 0
    reliability = get_sub_reliability(reliability_matrix, option)
    rel = reliability  # Add to list later
    for subset, sub_reliability in subsets:
        is_subset, probability = part_of(subset, option, reliability_matrix)
        if is_subset:
            subset_reliability = (probability * sub_reliability)
            reliability += subset_reliability
            if reliability > 1:
                raise Exception("Issue in get_reliability")
    subsets.append((option, rel))
    return reliability


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
print("Method: Brute force")

# Listing all options
# Each option is a matrix of boolean to indicate which edge is included
options = []
for i in range(num_of_cities - 1, 0, -1):
    options = add_line(options, bool_combinations(i))
options = [make_square_matrix(option, num_of_cities) for option in options]
# print("Number of configurations:", len(options))

subsets = []
counter = 0
best_reliability = 0
best_cost = 0
best_option = None
print("Finding the best configuration for a maximum cost of ", cost_limit)

for option in reversed(options):
    cost = get_cost(cost_matrix, option)  # Get the cost of a design choice
    valid, nodes = get_valid(option)
    if valid and cost <= cost_limit:
        counter += 1
        # reliability = get_reliability(reliability_matrix, option, subsets)  # Get reliability of a design choice
        reliability = getProbability(option, reliability_matrix)
        if best_reliability < reliability:
            best_reliability = reliability
            best_cost = cost
            best_option = option
        if verbose:
            print(f"Valid Option {counter}:")
            print("Option: " + str(option))
            print(f"Valid: {valid}")
            print(f"Nodes: {nodes}")
            print(f'Reliability: {reliability}')
            print(f'Cost:{cost}')
            print("\n")

print(f"Found {counter} valid options.")
if counter == 0:
    print("INFEASIBLE: Cost goal is infeasible")
else:
    print(f'Best Reliability: {best_reliability}')
    print("Best Cost: ", best_cost)
    print_matrix(best_option, "-----")

print(f'time taken: {(time.time() - t1)}')
