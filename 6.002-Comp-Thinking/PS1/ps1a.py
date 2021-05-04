###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    #Implement an empty dictionary
    cowDict={}
    #Create a file object that is read only of the data - using with as it automatically closes the file once finished
    with open(filename, "r") as cowList:
        for line in cowList:
            #strip removes ending "\n"
            cow = line.strip().split(",")
            cowDict[cow[0]]=int(cow[1])
    return cowDict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #Sort the dictionary and copy it into a list 
    #sorted returns a new list, cows.items() changes dict of cows into a list with tuples for each item, which is then iterated over by sorted, which by default sorts items in ascending order so reverse=true puts that into descending order. the key function is used to specify the value that should be sorted by, taking the item as the argument and returning the 2nd tuple value (weight)
    #complexity: n log(n)
    orderedCowList = sorted(cows.items(), key=lambda item: item[1], reverse=True)
    #Create a class that handles spaceships, to return them as a list of lists at the end
    #Create a class that handles adding cows, total weight and if cows should be added
    class Spaceship(object):
        def __init__(self, l=10, w=0, p=[]):
            self.limit = l
            self.weight = w
            self.passengers = p
        def getWeight(self):
            return self.weight
        def getLimit(self):
            return self.limit
        def getPassengers(self):
            #Returns the list stored in self.passengers, with only cow names, no as tuples
            return [cow[0] for cow in self.passengers]
        def addPassenger(self, cow):
            """
            Arg: cow=tuple. 
            Appends cow to the list stored in self.passengers
            Adds weight to self.weight to keep total weight
            """
            self.passengers.append(cow)
            self.weight += cow[1]
        def spaceLeft(self, cow):
            """ Arg: cow=number - representing weight of cow
                Returns boolean; True if cow can be added"""
            return self.getWeight() + cow[1] <= self.getLimit()
                


    result = [Spaceship(10)]
    #go through ordered list of cows (therefore this is linear complexity)
    for i in orderedCowList:
        borded = False
        #go through result, once a spaceship has enough space add it then exit loop,
        for s in result:
            if s.spaceLeft(i):
                s.addPassenger((i))
                borded=True
                break
        #If no spaceship had enough space make a new spaceship, append to end of result
        if(borded == False):
            result.append(Spaceship(10, w=i[1], p=[(i)]))
    #use list comprehensions to make a new list, converting the instances into lists
    return [i.getPassengers() for i in result]

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    bestShipNum = float("inf")
    #all possible permutations is 2**n+1 - exponential :(
    for partition in get_partitions(cows):
        #Keep track of number of spaceships
        ships = 0
        aboveLimit = False
        for ship in partition:
            ships += 1
            #Calculate the weight by refrencing the name in the dictionary and get the value pair - keep a tally per ship
            weight = 0
            for cow in ship:
                weight += cows[cow]
            if weight > limit:
                aboveLimit = True        
        if aboveLimit == False and bestShipNum>=ships:
            result = partition
            bestShipNum = ships
    return result
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cowDict = load_cows("ps1_cow_data.txt")
    # greedy_cow_transport test
    start = time.time()
    ## code to be timed
    spaceshipGreedy = greedy_cow_transport(cowDict, 10)
    end = time.time()
    print(end - start)
    print(spaceshipGreedy, len(spaceshipGreedy))

    #brute_force_cow_transport test
    start = time.time()
    ## code to be timed
    spaceshipBrute = brute_force_cow_transport(cowDict)
    end = time.time()
    print(end - start)
    print(spaceshipBrute, len(spaceshipBrute))

#TESTS
# cowDict={"Maggie": 3, "dave": 7, "tim": 10, "liv": 6, "jim": 2}
compare_cow_transport_algorithms()


