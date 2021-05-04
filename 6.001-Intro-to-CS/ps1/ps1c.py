# To be clear this code takes a salary input, presumes you save 4% and raise 7 %, and then finds outt how much your interest on savins must be for you to be able to afford a house in 36 months if it costs a million and the downpayment is 25%, usin a bisection recursive searching through 0-10000.
"""
I think I can solve this recursively, the thing you are breaking down is the amount of numbers, to find the one in 1000 I just need to check if it is 1 of them.
start at 500, the top is 1000, the bottom is 0, then divide answer by 1000 and calculate how much you would have by the end of 36 months. if bigger than down_payment then  make top that number, if smaller then make bottom that number, if top - bottom < 1 then return the number of top divided by 1000 and this will be then interst paid.
"""
annual_salary = float(input("Starting annual salary: "))
cost_of_house = 1000000
total_cost = cost_of_house * 0.25 #down payment
semi_annual_raise = 0.07
portion_saved = 0.04
annual_savings = annual_salary * portion_saved

def savings (r, annual_salary = annual_salary, annual_savings = annual_savings, portion_saved = portion_saved):
  current_savings = 0
  for i in range(1,37):
    current_savings += annual_savings/12
    current_savings = current_savings * (r/10000+1)
    if i % 6 == 0:
      annual_salary *= (semi_annual_raise + 1)
      annual_savings = annual_salary * portion_saved
  # print(current_savings)
  return current_savings
counter = 0
def bisection_search (bottom = 0.0, top = 10000.0, counter = counter):
  r = (bottom + top) / 2
  current_savings = savings(r)
  if current_savings - total_cost > -100 and current_savings - total_cost < 100:
    return (r/10000, counter + 1)
  elif current_savings > total_cost and top - bottom > 1:
    return bisection_search(bottom, r, counter + 1)
  elif current_savings < total_cost and top - bottom > 1:
    return bisection_search(r, top, counter + 1)

# We must return a tuple, with the first element being the result in percentage and the second the amount of searches.
result = bisection_search()
percentage = round(result[0],4)
print("with a starting salry of: " + str(annual_salary))
print("You must make " + str(percentage) + "% per month to afford the down payment on your dream home in three years.")
print("Number of bisection calls: " + str(result[1]))


  