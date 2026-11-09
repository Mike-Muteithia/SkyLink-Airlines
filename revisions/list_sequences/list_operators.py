# num = [1, 2, 3, 4, 5]
# lang = ['python', 'c', 'java', 'php']

# print(num + lang)   #concatenates two lists - (concatenation operator)
# print(num * 2)    # concatenates same list 2 times - (repetition operator)
# print(lang[2])    # prints 2nd index value - (slice operator)
# print(lang[1 : 4])    # print values from 1st to 3rd index - (range slice operator)
# print('cpp' in lang)    # prints False - (membership operator)
# print(6 not in num)   # prints True - (membership operator)


## How to update or change elements to a list - (slice and assignment operator)
# num = [1, 2, 3, 4, 5]
# print(num)

# num[2] = 30
# print(num)

# num[1 : 3] = [25, 36]
# print(num)

# num[4] = "Python"
# print(num)


## How to delete or remove elements from a list - (del)
# num = [1, 2, 3, 4, 5]
# print(num)

# del num[1]
# print(num)

# del num[1 : 3]
# print(num)


## Iterating a list - (for - in)
lang = ['python', 'c', 'java', 'php']
print("The list items are \n")
for i in lang:
  print(i)
