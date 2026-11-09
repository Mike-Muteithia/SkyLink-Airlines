### 1. Concept & Syntax Check

## 1. 
# a. a comma 
# b. [] 
# c. 0 
# d. -1

## 2. 
# a. + operator concatenates two different lists, while * operator concatenates the same list twice
# b. 'in' and 'not in'

## 3. 
# a. the first occurence
# b. the output gives an error
# c. remove() gives an error, while list.count(item) outputs 0

## 4.
# a. sort(reverse = true)
# b. Unlike sorting that arranges in ascending or descending order, list.reserve() just reverses the order, with rightmost element going first and the first element being last.


### 2. Spot & Fix Bug

## 1. Cannot add str and int since '30' is a str, and 50 does not exist in scores

## 2. For num.insert(25, 1), it is num.insert(item, index) instead of num.insert(index, item), and instead of removing the element in index 3, num.pop(5) removes the element in index 5 which does not exist, thus giving an error.
# Correct syntax:
# num = [10, 20, 30]
# num.insert(1, 25)
# num.pop(3)
# print(num)


### 3. Output Prediction & Coding Challenges

## 1.
# a. ['apple', 'mango']
# b. [1, 25, 36, 5]

## 2. 
num = [6, 8, 2, 4]
num.append(10)
print(num)
print("The length of num:", len(num))
print("The max of num:", max(num))
print("The min of num:", min(num))

## 3.
word = "banana"
list1 = list(word)
print(list1)
print(list1.count('a'))
for i in list1:
  print(i)
