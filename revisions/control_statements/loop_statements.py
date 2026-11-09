### while loop
## Syntax
# while expression:
#     Statement(s)

## Ex1
# i = 1;

# while i <= 3:
#     print(i);
#     i = i + 1;

## Using else with while loop
# i = 1;

# while i <= 3:
#     print(i);
#     i = i + 1;
# else:
#     print("while loop terminated")


### for loop
## Syntax
# for iterating_var in sequence:
#     statement(s)

## Ex1
# i = 1
# n = int(input("Enter n value: "))

# for i in range(i, n + 1):
#     print(i, end = ' ')

## Using else with for loop
for i in range(1, 100):
    print(i, end = '  ')
else:
    print("for loop completely exhausted")
