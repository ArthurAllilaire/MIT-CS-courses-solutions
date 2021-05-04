###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1 - this could be done faster as a greedy algorithm
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #Check for the base case
    if target_weight == 0:
        #no more eggs needed to be added
        return 0
    #if there is still weight left but not any possible values to be stored return false (it wasn't possible)
    if egg_weights == ():
        return False
    #check if problem has already been solved, if so return that solution
    if target_weight in memo:
        return memo[target_weight]
    #if can't put the heaviest egg don't explore the left branch
    if egg_weights[-1] > target_weight:
        withoutEgg = dp_make_weight(egg_weights[:-1], target_weight, memo)
    else:
        next_item = egg_weights[-1]
        #explore left branch and add 1 to number as added an egg
        withEgg = dp_make_weight(egg_weights, target_weight - next_item, memo) + 1
        #explore right branch - not needed as greedy algorithm - this solution will never be better
        withoutEgg = dp_make_weight(egg_weights[:-1], target_weight, memo)
        #Check withoutEgg completed the problem
        #compare the branches
        if withoutEgg == False or withEgg < withoutEgg:
            #add best to memo
            memo[target_weight] = withEgg
            return withEgg
    memo[target_weight] = withoutEgg
    return withoutEgg

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()