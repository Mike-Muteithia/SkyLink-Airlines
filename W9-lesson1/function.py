### Creating a Function & Calling a Function

# def student():
#   print("My name is ...")
# print("My school is ...")


# student() # Calling a function

# Can be called multiple times
# student()
# student()
# student()


### Function Names - another reason to comment your code


### Why use functions

## Without functions
# temp1 = 77
# celsius1 = (temp1 - 32) * 5 / 9
# print(celsius1)

# temp2 = 95
# celsius2 = (temp2 - 32) * 5 / 9
# print(celsius2)

# temp3 = 50
# celsius3 = (temp3 - 32) * 5 / 9
# print(celsius3)

## With functions
# def fahrenheit_to_celsius(fahrenheit):
#   return (fahrenheit - 32) * 5 / 9

# print(fahrenheit_to_celsius(77))
# print(fahrenheit_to_celsius(95))
# print(fahrenheit_to_celsius(50))


### Return Values
# def get_greeting():
#   return "Hello from a function"

# print(get_greeting())


### Pass Statement
# def my_function():
#   pass


### Arguements
# def my_function(fname):
#   print(fname + " Refsnes") # one agrument

# my_function("Emil")
# my_function("Tobias")
# my_function("Linus")


### Parameters vs Agruments
# A parameter is the variable listed inside the parentheses in the function definition.
# An argument is the actual value that is sent to the function when it is called

def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an arguement
