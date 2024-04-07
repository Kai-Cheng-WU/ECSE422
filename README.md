# ECSE422 Network Design Project

| Name | Student ID |
|-----------------|-----------------|
| Andrei Sandor | 260977451  |
| Nitin Kaundun |  260786113 |
| Kaicheng Wu | 260892789 |


## Prerequisite:
Any version of python
### Installation of Python3 for Mac OS Using Homebrew:
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
brew install python` 
 
Use the following command to make sure that python is installed: \
`python3 --version`


## To run the code: 
### Version 1 - Brute Force 
<p>The python script can be called without any command line argument.</p>

`python networkDesign.py input_file.txt`\
OR \
`python3 networkDesign.py input_file.txt`

<p>These arguments can also be passed in order. Otherwise, their value remains as default.</p>

`python networkDesign.py input_file.txt cost_limit Verbose`\
OR \
`python3 networkDesign.py input_file.txt cost_limit Verbose`

1. Input_file.txt - your input file with the configuration. **Default: 4_city.txt**
2. cost_limit - an integer value which is the target goal for the cost. **Default: 85**
3. Verbose - boolean value. If set to true, all the valid (cost within goal and Rall != 0) configurations are listed. If set to false, only the  best config is shown. **Default: False**

### Version 2 - MST and augmentation
<p>Same as before, the python script can be called with or without any command line argument.</p>

`python networkDesignV2.py input_file.txt`\
OR \
`python3 networkDesignV2.py input_file.txt`

<p>These arguments can also be passed in order. Otherwise, their value remains as default.</p>

`python networkDesignV2.py input_file.txt cost_limit Verbose`\
OR \
`python3 networkDesignV2.py input_file.txt cost_limit Verbose`

# Execution Traces
The outputs of executions for the bruteforce algorithm can be found in the brute folder, version 2 in PrimmV2, version 3 in PrimmV3.

# TODO

Provide a very detailed README. It should give me precise step-by-step instructions.
Provide a sample execution trace for each input files and for the two different versions.

## Exhaustive Enumeration
The first thing that we do for exhaustive enumeration is to collect the inputs from the command line. The first input is the filename, the second is the cost limit (we will consider a <= case) and the third is verbose which if set to True, it will print all the valid options we have for exhaustive enumeration (i.e those that all cities are connected). A verbose set to False only outputs the best optimal option for exhaustive enumeration. Then, we will parse the file inputed by extracting the number of cities, by creating a list of reliability and by creating a list of cost. Then, we will convert those into square matrices. The matrices will contain values in the upper triangular part and dashes on the lower triangular part.

e.g. 
<br> - 10 15 
<br> -  - 5 
<br> -  -  - 

Then, we will generate all the options. We will start from all the edges not included and we will start to include edge by edge until we get to all edge selected. For example, if we have 4 cities, the first option will be [[0,0,0],[0,0],[0]], then [[0,0,0],[0,0],[1]], then [[0,0,0],[0,1],[0]], [0,0,0,0,1,1] and so on until [[1,1,1],[1,1],[1]]. Then, each option will be transformed into a matrix of booleans to indicate which edge is included. An edge not included is 0/False and an edge included is a 1/True. We fill with None the rest to get a nice matrix.

e.g 
<br> None True False
<br> None None True
<br> None None None

We will start from the first option [0,0,0,0,0,0] and move our way up. First, we will get the cost of the option. We will go edge after edge included by using the cost matrix to find the total cost. After, we will check if this option is valid (i.e it connects all the cities) by doing a BFS. If not, we go to generate the next option. If yes, we find its probability. Since the first ones we obtain are MST, the probability will be simplied calculated by multiplying the reliabilites of the edges. After those MST cases, we compute our reliability by using what we found from an MST/previous calculation of not a minimum spanning tree by considering the edge that we added to the connection. We will do this until we get everything (there will be a check on the cost limit). At the end, we will chose the best result that will look something like this.


<img width="997" alt="Screenshot 2024-04-01 at 3 07 55 PM" src="https://github.com/Kai-Cheng-WU/ECSE422/assets/97865484/2f9534b9-315d-40c9-868b-93c4ab365744">

The last input gives the output in a matrix form.

## Better Algorithm

For the better algorithm, we did the same parsing as in the exhaustive enumeraion to get the cost and reliability matrices. 

For the better algorithm, we combined three different heuristic ideas.

The first one is a greedy by cost approach. First, we generate the MST by using Kruskal like in class. We ordered from smallest cost to highest cost and we create a MST without redundancy. After that, we decided to augment by always going with the one with the best cost until the maximum cost limit is reached.

The second one is a greedy by reliability approach. First, we generate the MST by using Kruskal like in class. From the MST, we compute the reliability of all possible graph with one additional edge and pick the one with the highest reliability and continue to expand it. We then iteratively augment the graph until we reach the maximum cost limit.

The third one is a greed by best reliability to cost approach. The idea is somewhat similar to the reliability approach. First, we generate the MST by using Kruskal like in class. We then compute the reliability of all possible graph with one additional edge, however, this time we would select the graph with the highest reliability to cost ratio and expand it from there. As before, we iteratively repeat this process until the maximum cost limit is reached. 

For each of these approaches we find the best probability like we did in part 1. After, we compare the best three results and we decide to work with the best approach which we will output. 

## Interesting approach

We decided to add three better algorithms for the better algorithm part since we might get better results than using only one
