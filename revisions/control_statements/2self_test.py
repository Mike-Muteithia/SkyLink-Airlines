### 1. Concept & Syntax Check
## 1. Answers: a. An indentation, b. Tab and four spaces

## 2. Answers: a. while, b. for

## 3. Answers: The break statement breaks loops one by one -- it breaks the inner loop first and then proceeds to the outer loops

## 4. Else would not execute when break comes before it.

### 2. Spot & Fix the Bug
## 1. Answer: the age variable is not converted into a integer with int() and the if condition is missing ':' to end the if condition statement.

## 2. 'i = i + 1' was not been nested inside the while loop, thus 'i <= 3' does not limit it.

### 3. Output Prediction & Coding Challenges
## 1. Output: 1 3 4 while loop terminated

## 2. Answer:
n = int(input("Enter a number: "))

if (n > 0) and (n < 10):
    print("Single digit positive")
elif (n >= 10) and (n < 100):
    print("Double digit positive")
else:
    print("Other number")

## 3. Answer:
user_str = str(input("Enter any String: "))

for i in user_str:
    if i == 'e':
        continue
    print(i, end = " ")

