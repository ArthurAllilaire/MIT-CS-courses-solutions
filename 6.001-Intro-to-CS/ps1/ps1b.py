annual_salary = float(input("Starting annual salary: "))
portion_saved = float(input("Portion saved (in decimal): "))
total_cost = float(input("total cost of house: "))
semi_annual_raise = float(input("Semi annual raise (in decimal): "))
annual_savings = annual_salary * portion_saved
down_payment = 0.25 * total_cost
current_savings = 0
r = 0.04 / 12
total_months = 0
while down_payment>current_savings:
  current_savings += annual_savings/12
  current_savings = current_savings * (r+1)
  total_months += 1
  if total_months % 6 == 0:
    annual_salary *= (semi_annual_raise + 1)
    annual_savings = annual_salary * portion_saved

print("it will take you " + str(total_months) + " months to save up for your house.")