"""
So, I didn't understand the question asked, so we are going to have to tweak my code, we are now tryin to find what % of salary person should save to be able to afford house.
"""
annual_salary = float(input("Starting annual salary: "))
cost_of_house = 1000000
total_cost = cost_of_house * 0.25 #down payment

def savings (portion_saved, annual_salary = annual_salary):
  current_savings = 0
  semi_annual_raise = 0.07
  annual_savings = annual_salary * portion_saved
  interest_per_month = 0.04 / 12
  for i in range(1,35):
    current_savings += annual_savings/12
    current_savings = current_savings * interest_per_month
    if i % 6 == 0:
      annual_salary *= (semi_annual_raise + 1)
      annual_savings = annual_salary * portion_saved
  # print(current_savings)
  return current_savings
counter = 0
def bisection_search (bottom = 0.0, top = 10000.0, counter = counter):
  r = (bottom + top) / 2
  current_savings = savings(r)
  if top + bottom >= 19999:
    return (None, counter + 1)
  elif current_savings - total_cost > -100 and current_savings - total_cost < 100:
    return (r/10000, counter + 1)
  elif current_savings > total_cost:
    return bisection_search(bottom, r, counter + 1)
  elif current_savings < total_cost:
    return bisection_search(r, top, counter + 1)

# We must return a tuple, with the first element being the result in percentage and the second the amount of searches.
print("with a starting salry of: " + str(annual_salary))
result = bisection_search()
if result[0] != None:
  percentage = round(result[0],4)
  print("You must save " + str(percentage) + "% of your salary to afford the down payment on your dream home in three years.")
else:
  print("You are not able to achieve your dream home on your current salary in three years.")
print("Number of bisection calls: " + str(result[1]))