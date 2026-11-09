## Type Casting

# int() - converts any data type to an integer
# float() - converts any data typrs to a floating point number
# str() - converts any data type to a string

# x = int(2.8)
# y = int("3")
# z = float(2)
# s = str(10)

# print(x, y, z, s)

# s1 = type(s)

# print(s1)


# Practice
# int()
price_float = 19.99
quantity_str = "5"

price_int = int(price_float)
quantity_int = int(quantity_str)

print("Integer price:", price_int, type(price_int))
print("Integer quantity:", quantity_int, type(quantity_int))

# float()
score_int = 95
rate_str = "4.5"

score_float = float(score_int)
rate_float = float(rate_str)

print("Float score:", score_float, type(score_float))
print("Float rate:", rate_float, type(rate_float))

# str()
age = 25
message = "User age is " + str(age)
print(message, type(message))