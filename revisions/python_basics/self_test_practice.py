## Exercise 1
item_price = "150"
tax_rate = "12.5"

# Solution1
# item_price_float = float(item_price)
# print(item_price_float)

# tax_rate_float = float(tax_rate)
# print(tax_rate_float)

# total = item_price_float + tax_rate_float

# total_str = str(total)

# print("Total price is", total_str)

# Solution2
# total_cost = int(item_price) + float(tax_rate)
# print("Total price is " + str(total_cost))


## Exercise 2
# total_seconds = 500

# minutes = total_seconds // 60
# print(minutes)

# remaining_seconds = total_seconds % 60
# print(remaining_seconds)

# print("Minutes:", minutes, "; Remaining Seconds:", remaining_seconds)

## Exercise 3
a = "10"
b = 5

a = int(a)
print(a, type(a))

a *= 2
print(a)

ans = a > b and a % 4 == 0
print(ans)


