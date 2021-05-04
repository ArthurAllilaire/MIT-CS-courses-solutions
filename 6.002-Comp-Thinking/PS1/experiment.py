from ps1a import greedy_cow_transport


cowDict={"Maggie": 3, "dave": 7, "tim": 10, "liv": 6, "jim": 2}


spaceship = greedy_cow_transport(cowDict, 10)
print(spaceship)
#lambda cowDict: cowDict[1]