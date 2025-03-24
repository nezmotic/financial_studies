import math

capital = 500000
annual_return_stocks = 0.08
inflation = 0.027
credit_period = 25
house_price = 500000
rental_yield = 0.04
interest = 0.037
leverage_ratio = 0.8
tax_rate = 0.25
post_period = 25

capital_end_nominal = capital * math.pow(1 + annual_return_stocks, credit_period)
capital_end_real = capital * math.pow(1 + annual_return_stocks - inflation, credit_period)
print(f"capital_end_nominal: {capital_end_nominal}")
print(f"capital_end_real: {capital_end_real}")

rent = house_price * rental_yield * (1/12)

#Scenario 1: Buy house with cash

capital_temp = 12 * rent * (math.pow((annual_return_stocks - inflation) + 1, credit_period) - 1) / (annual_return_stocks - inflation)
revenue = capital_temp - 12 * credit_period * rent
capital_end_cash = capital_temp - tax_rate * revenue
print(f"capital_end_cash: {capital_end_cash}")
#post period
capital_temp = capital_temp * math.pow(1 + annual_return_stocks - inflation, post_period)
capital_temp = capital_temp + 12 * rent * (math.pow((annual_return_stocks - inflation) + 1, post_period) - 1) / (annual_return_stocks - inflation)
revenue = capital_temp - 12 * rent * (credit_period + post_period)
capital_post_cash = capital_temp - tax_rate * revenue
print(f"capital_post_cash: {capital_post_cash}")

#Scenario 2: Buy house with credit

credit = leverage_ratio * house_price
annuity = credit * ((interest - inflation) * math.pow(1 + interest - inflation, credit_period)) / (math.pow(1 + interest - inflation, credit_period) - 1)
credit_rate = annuity * (1/12)
dissaving_rate = credit_rate - rent
capital_start = capital - (house_price - credit)
capital_temp = capital_start

for year in range(credit_period):
    capital_temp -= 12 * (dissaving_rate * (1 + tax_rate * (capital_temp - capital_start)/capital_start))
    capital_temp *= 1 + annual_return_stocks - inflation

revenue = capital_temp - capital_start
capital_end_credit = capital_temp - revenue * tax_rate
print(f"capital_end_credit: {capital_end_credit}")
#post period
capital_temp = capital_temp * math.pow(1 + annual_return_stocks - inflation, post_period)
capital_temp = capital_temp + 12 * rent * (math.pow((annual_return_stocks - inflation) + 1, post_period) - 1) / (annual_return_stocks - inflation)
revenue = capital_temp - capital_start + 12 * post_period * rent
capital_post_credit = capital_temp - revenue * tax_rate
print(f"capital_post_credit: {capital_post_credit}")

#Scenario 3: Rent

capital_temp = capital * math.pow(1 + annual_return_stocks - inflation, credit_period)
revenue = capital_temp - capital
capital_end_rent = capital_temp - revenue * tax_rate
print(f'capital_end_rent: {capital_end_rent}')
#post period
capital_temp = capital_temp * math.pow(1 + annual_return_stocks - inflation, post_period)
revenue = capital_temp - capital
capital_post_rent = capital_temp - revenue * tax_rate
print(f'capital_post_rent: {capital_post_rent}')






