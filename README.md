# ECSE422 Network Design Project

| Name | Student ID |
|-----------------|-----------------|
| Andrei Sandor | 260977451  |
| Nitin Kaundun |   |
| Kaicheng Wu | 260892789 |


## Prerequisite:
Any version of python
### Installation of Python3 for Mac OS Using Homebrew:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" \
brew install python 
 
Use the following command to make sure that python is installed: \
python3 --version


## To run the code: 
python networkDesign.py input_file.txt \
OR \
python3 networkDesign.py input_file.txt

## Exhaustive Enumeration
The first thing that we do for exhaustive enumeration is to collect the inputs from the command line. The first input is the filename, the second is the cost limit (we will consider a <= case) and the third is verbose which if set to True, it will print all the valid options we have for exhaustive enumeration (i.e those that all cities are connected). A verbose set to False only outputs the best optimal option for exhaustive enumeration. Then, we will parse the file inputed by extracting the number of cities, by creating a list of reliability and by creating a list of cost. Then, we will convert those into square matrices. The matrices will contain values in the upper triangular part and dashes on the lower triangular part.

e.g. 
<br> - 10 15 
<br> -  - 5 
<br> -  -  - 

Then, we will generate all the options. We will start from all the edges not included and we will start to include edge by edge until we get to all edge selected. For example, if we have 4 cities, the first option will be [0,0,0,0,0,0], then [0,0,0,0,0,1], then [0,0,0,0,1,0], [0,0,0,0,1,1] and so on until [1,1,1,1,1,1]. Then, each option will be transformed into a matrix of booleans to indicate which edge is included. An edge not included is 0/False and an edge included is a 1/True. We fill with None the rest to get a nice matrix.

e.g 
<br> None True False
<br> None None True
<br> None None None

We will start from the first option [0,0,0,0,0,0] and move our way up. First, we will get the cost of the option. We will go edge after edge included by using the cost matrix to find the total cost. After, we will check if this option is valid (i.e it connects all the cities). If not, we go to generate the next option. If yes, we find its probability. Since the first ones we obtain are MST, the probability will be simplied calculated by multiplying the reliabilites of the edges. After those MST cases, we compute our reliability by using what we found from an MST/previous calculation of not a minimum spanning tree by considering the edge that we added to the connection. We will do this until we get everything (there will be a check on the cost limit). At the end, we will chose the best result that will look something like this.


<img width="997" alt="Screenshot 2024-04-01 at 3 07 55 PM" src="https://github.com/Kai-Cheng-WU/ECSE422/assets/97865484/2f9534b9-315d-40c9-868b-93c4ab365744">

The last input gives the output in a matrix form.

 

