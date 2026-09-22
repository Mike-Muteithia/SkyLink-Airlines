## append() method - adds an item to the end of a list
#                  - list.append(item)

# num = [1, 2, 3, 4, 5, 6]
# lang = ['python', 'c', 'java']

# num.append(7)
# print(num)

# lang.append("cpp")
# print(lang)


## remove() method - removes an item from a list
#                  - removes first occurrence of an item if the list contains duplicates
#                  - throws an error if the item is not present in the list
#                  - list.remove(item)

# list1 = [1, 2, 3, 4, 5]
# list2 = ['A', 'B', 'C', 'B', 'D']

# list1.remove(2)
# print(list1)

# list2.remove("B")
# print(list2)

# list2.remove("E")
# print(list2)


## sort() method - sorts the list elements into descending or ascending order
#                - sorts the elements in ascending order by default
#                - takes an optional parameter 'reverse' 
#                  which sorts the list in descending order
#                - list.sort([reverse = true])

# list1 = [6, 8, 2, 4, 10]

# list1.sort()
# print("\n After Sorting: \n")
# print(list1)

# print("\n Descending Order: \n")
# list1.sort(reverse = True)
# print(list1)


## reverse() method - reverses elements of a list
#                   - the last index of a list will be present at 0th index
#                   - list.reverse()

# list1 = [9, 12, 15, 6, 3, 18, 24]
# list1.reverse()

# print("\n After reverse: \n")
# print(list1)


## count() method - returns the number of times an element appears in a list
#                 - if the element is not present in the list, it returns 0
#                 - list.count(item)

# num = [1, 2, 4, 8, 2, 5, 8, 9, 1, 4, 2, 6, 8, 2]

# cnt = num.count(2)
# print("Count of 2 is: ", cnt)

# cnt = num.count(10)
# print("Count of 10 is: ", cnt)


## index() method - returns index of the passed element
#                   - raises a ValueError if the element is no present
#                   - returns index of first occured element if there are duplicates
#                   - takes two more optional paraments start and end
#                     which search index within a limit
#                   - list.index(item, start, end)

# list1 = ['c', 'o', 'n', 'c', 'e', 'n', 't', 'r', 'a', 't', 'i', 'o', 'n']

# print(list1.index('e'))
# print(list1.index('n'))
# print(list1.index('n', 3, 10))
# print(list1.index('f'))


## insert() method - inserts an element at the specified index in a list
#                    - the first agrument is the index of the element before
#                      which to insert the element
#                    - list.insert(index, item)

# num = [15, 30, 45, 60, 75, 90]

# num.insert(3, 66)
# print(num)

# num.insert(7, 105)
# print(num)


## pop() method - removes an element present at a specified index fom a list
#               - list.pop(index)

# num = [11, 22, 33, 44, 55, 66, 77]

# num.pop()
# print(num)

# num.pop(4)
# print(num)

# num.pop(8)
# print(num)


## clear() method - removes all the elements from a list
#                 - clears the list completely and returns nothing
#                 - list.clear()

num = [12, 24, 36, 48, 60, 72, 84, 96]

num.clear()
print(num)