#big(O) = linear (-1 for base case) steps along the thing 
# ln = ln-1 + ln
string="123"
#get permutation of 12, to do that get permutation of 1, return 1 as its length is one, then for 12 put 2 in front, and behind, return an array, with: ["1", (add first permutation without adding) "12", "21"], go through the process again.
def perm(a):
  if len(a) == 0:
    return [a]
  #else get the permutation of all of the substring n-1 - that is an array
  permBelow = perm(a[:len(a)-1])
  result = []
  lastLetter = a[len(a)-1]
  #insert last letter of a in all possible values - linearly go through list
  for i in permBelow:
    for c in range(len(i)+1):
      #add character that isn't in 
      result.append(
        i[:c] + lastLetter + i[c:]
      )
  return permBelow + result  

# Go through the list, getting bigger every time, then

#You need a base case, which is the first value given, you then add that value to every other before permutation in all the given spots 

def valuePerm(a):
  if len(a) == 0:
    return [a]
  permBelow = valuePerm(a[:-1])
  result = []
  lastLetter = a[-1]
  #insert last letter of a in all possible values - linearly go through list
  for i in permBelow:
    #add character that isn't in 
    result.append(
      i + lastLetter
    )
  return permBelow + result

print(perm(string))
print(valuePerm(string))