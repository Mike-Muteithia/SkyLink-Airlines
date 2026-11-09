## append() - list.append(item) - (adds an item to the end of the list)
# num = [1, 2, 3, 4, 5]
# lang = ['python', 'java']

# num.append(6)
# print(num)

# lang.append("cpp")
# print(lang)


## remove() - list.remove(item) - (removes item from the list)
# list1 = [1, 2, 3, 4, 5]
# list2 = ['A', 'B', 'C', 'B','D']

# list1.remove(2)
# print(list1)

# list2.remove("B")
# print(list2)

# list2.remove("E")
# print(list2)


## sort() - list.sort([reverse = true]) - (sorts the list elements into descending or ascending order)
# list1 = [6, 8, 2, 4, 10]

# list1.sort()
# print("\n After Sorting:\n")
# print(list1)

# print("\n Descending Order:\n")
# list1.sort(reverse = True)
# print(list1)


## reverse() - list.reverse() - (reverses elements of the list)
# list1 = [6, 8, 2, 4, 10]
# list1.reverse()

# print("\n After reverse:\n")
# print(list1)


## count() - list.count(item) - (returns the number of items an element appears in the list)
# num = [1, 2, 3, 4, 3, 2, 2, 1, 4, 5, 8]

# cnt = num.count(2)
# print("Count of 2 is:", cnt)

# cnt = num.count(10)
# print("Count of 10 is:", cnt)


## index() - list.index(item[, start[, end]]) - (returns index of the passed element)
# list1 = ['p', 'y', 't', 'o', 'n', 'p']

# print(list1.index('t'))
# print(list1.index('p'))
# print(list1.index('p', 3, 10))
# print(list1.index('z'))


## insert() - list.insert(index, item) - (inserts the element at the specified index in the list)
# num = [10, 20, 30, 40, 50]

# num.insert(4, 60)
# print(num)

# num.insert(7, 70)
# print(num)


## pop() - list.pop(index) - (remove an element present at specified index from the list)
# num = [10, 20, 30, 40, 50]

# num.pop()
# print(num)

# num.pop(2)
# print(num)

# num.pop(7)
# print(num)


## clear() - list.clear() - (removes all the elements from the list)
num = [10, 20, 30, 40, 50]

num.clear()
print(num)

