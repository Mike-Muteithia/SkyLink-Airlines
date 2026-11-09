## 1
# m1 = int(input("Enter your first score: "))
# m2 = int(input("Enter your second score: "))
# m3 = int(input("Enter your third score: "))

# average_score = int((m1 + m2 + m3) / 3)
# print("Average:", average_score)

# if average_score > 80:
#   print("GOOD")

## 2
# num = int(input("Enter a number: "))

# while num > 0:
#     print(num)
#     num -= 1

## 3: Print a multiplication table from 1 to 10 in a formatted grid
# for row in range(1, 11):
#   for col in range(1, 11):
#     print(row * col, end = "\t")
#   print()

## 4: Print the first 15 terms of the Fibonacci series (0, 1, 1, 2, 3, 5...)
# a, b = 0, 1

# for i in range(15):
#   print(a, end = "\t")
#   a, b = b, a + b

## 5: Check if a given number is a palindrome (e.g., 121, 545)
# num_str = input("Enter a number: ")

# list_str = list(num_str)
# reverse_list = list(num_str)
# reverse_list.reverse()

# if list_str == reverse_list:
#   print(num_str, "is a palindrome")
# else:
#   print(num_str, "is not a palindrome")

## 6
# nums = [1, 2, 3, 2, 4, 3, 6, 8, 2]
# unique = []

# for i in nums:
#   if i not in unique:
#     unique.append(i)
# print(unique)

## 7: Single-line list comprehension that filters out strings shorter than 4 characters and converts the rest to uppercase
# words = ["dog", "trunk", "manga", "triangle", "highway"]

# result = [w.upper() for w in words if len(w) >= 4]

# print(result)

## 8: Create a function that takes a string and returns a character count (ignoring spaces, case-insensitive)
# def count_characters(text):
#   text = text.lower()
#   counts = {}

#   for char in text:
#     if char == " ":
#       continue
#     if char in counts:
#       counts[char] += 1
#     else:
#       counts[char] = 1
#   return counts

# print(count_characters("Hello World"))

## 9: Explain the LEGB rule in Python with a code example demonstrating all four scopes
# global_var = "I am Global"

# def outer():
#   enclosing_var = "I am Enclosing"

#   def inner():
#     local_var = "I am Local"

#     print(local_var)
#     print(enclosing_var)
#     print(global_var)
#     print(len(global_var))

#   inner()

# outer()
