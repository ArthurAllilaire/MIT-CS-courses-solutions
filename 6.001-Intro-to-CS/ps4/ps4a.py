# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    permutations = []
    # If the sequence given is of length 1 then return it
    if len(sequence) == 1:
        permutations.append(sequence)
        return permutations
    # Else take all of the string minus the base case - for simplicity the first letter and get all the possible permutations, add it as a list
    smaller_sequence = sequence[1:]
    smaller_permutations = (get_permutations(smaller_sequence))
    # Then add the first letter to every possible position in each permutation given above, then return it as a list
    base_case = sequence[0]
    #loop over every permutation
    for i in smaller_permutations:
        # create a counter for every index
        for index in range(len(i)+1):
            #insert base case at every possible index
            permutation = i[:index] + base_case + i[index:]
            #append the permutation to a list of all possible permutations
            permutations.append(permutation)
    #return the list of all possible permutations
    return permutations



if __name__ == '__main__':
   #EXAMPLE
   example_input = 'abcd'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))
   input2 = 'hef'
   print('Input:', input2)
   print('Expected Output:', ['hef', 'hfe', 'fhe', 'ehf', 'efh', 'feh'])
   print('Actual Output:', get_permutations(input2))
   input4 = 'cdz'
   print('Input:', input4)
   print('Expected Output:', ['cdz', 'czd', 'zcd', 'dcz', 'dzc', 'zdc'])
   print('Actual Output:', get_permutations(input4))
   input3 = "d"
   print('Input:', input3)
   print('Expected Output:', ["d"])
   print('Actual Output:', get_permutations(input3)) 
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

 #delete this line and replace with your code here

