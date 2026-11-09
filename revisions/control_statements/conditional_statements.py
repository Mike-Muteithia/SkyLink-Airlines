### if
## Syntax
# if condition:
#     statement1
#     statement2

## Ex1
# a = 33
# b = 200

# if b > a:
#   print("b is greater than a")
#   print("done...")

## Remember
# input()

## Ex2
# a = input("Enter a value: ")
# print(a)


### if -- else
## Syntax
# if condition:
#   #block of statements
# else:
#   #another block of statements (else-block)

## Ex1
# age = int(input("Enter your age: "))

# if age >= 18:
#   print("You are eligble to vote!!!")
# else:
#   print("Sorry! You have to wait.")


### if -- elif -- else
## Syntax
# if condition1:
#   # block of statements
# elif condition2:
#   # block of statements
# elif condition3:
#   # block of statements
# else:
#   # block of statements

## Ex1
a = int(input("Enter a value: "))
b = int(input("Enter b value: "))
c = int(input("Enter c value: "))

if (a > b) and (a > c):
  print("Maximum value is: ", a)
elif (b > a) and (b > c):
  print("Maximum value is: ", b)
else:
  print("Maximum value is: ", c)

