# List Sequence in Python
Based on the lecture slides: List_Sequence_in_Python.pdf

## 1. List Creation
In Python, a list can be defined as a collection of values or items.
* The items in the list are separated with a comma (`,`) and enclosed within square brackets `[]`.

**Syntax:**
`list-var = [value1, value2, value3, ...]`

**Example: `listdemo.py`**
```python
L1 = []
L2 = [123, "python", 3.7]
L3 = [1, 2, 3, 4, 5, 6]
L4 = ["C", "Java", "Python"]

print(L1)
print(L2)
print(L3)
print(L4)
```

**Output:**
```text
[]
[123, 'python', 3.7]
[1, 2, 3, 4, 5, 6]
['C', 'Java', 'Python']
```

---

## 2. List Indexing
Like string sequences, the indexing of Python lists starts from 0. The first element of the list is stored at the 0th index, the second element is stored at the 1st index, and so on. The elements of the list can be accessed by using the slice operator `[]`.

**Example:**
`mylist = ["banana", "apple", "mango", "tomato", "berry"]`

| banana | apple | mango | tomato | berry |
|--------|-------|-------|--------|-------|
| 0      | 1     | 2     | 3      | 4     |

* `mylist[0] = "banana"`
* `mylist[2] = "mango"`
* `mylist[1:3] = ["apple", "mango"]`

### Negative Indexing (Backward Direction)
Unlike other languages, Python provides the flexibility to use negative indexing. The negative indices are counted from the right. The last element (rightmost) of the list has the index `-1`, its adjacent left element is present at the index `-2`, and so on until the leftmost element is encountered.

| Element | banana | apple | mango | tomato | berry |
|---------|--------|-------|-------|--------|-------|
| Forward | 0      | 1     | 2     | 3      | 4     |
| Backward| -5     | -4    | -3    | -2     | -1    |

* `mylist[-1] = "berry"`
* `mylist[-3] = "mango"`
* `mylist[-4:-2] = ["apple", "mango"]`

---

## 3. List Operators

| Operator | Name | Description |
|---|---|---|
| `+` | Concatenation | Used to concatenate two lists. |
| `*` | Repetition | Concatenates multiple copies of the same list. |
| `[]` | Slice | Used to access a specific list item. |
| `[:]` | Range Slice | Used to access a range of list items. |
| `in` | Membership | Returns true if a particular item is present in the list. |
| `not in` | Membership | Returns true if a particular item is NOT present in the list. |

**Example: `listopdemo.py`**
```python
num = [1, 2, 3, 4, 5]
lang = ['python', 'c', 'java', 'php']

print(num + lang)      # concatenates two lists
print(num * 2)         # concatenates same list 2 times
print(lang[2])         # prints 2nd index value
print(lang[1:4])       # prints values from 1st to 3rd index
print('cpp' in lang)   # prints False
print(6 not in num)    # prints True
```

**Output:**
```text
[1, 2, 3, 4, 5, 'python', 'c', 'java', 'php']
[1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
java
['c', 'java', 'php']
False
True
```

---

## 4. Modifying Lists

### Updating or Changing Elements
Python allows us to modify list items by using the slice and assignment operator `()=`. We can use the assignment operator to change an item or a range of items.

**Example: `listopdemo1.py`**
```python
num = [1, 2, 3, 4, 5]
print(num)

num[2] = 30
print(num)

num[1:3] = [25, 36]
print(num)

num[4] = "Python"
print(num)
```

**Output:**
```text
[1, 2, 3, 4, 5]
[1, 2, 30, 4, 5]
[1, 25, 36, 4, 5]
[1, 25, 36, 4, 'Python']
```

### Deleting or Removing Elements
Python allows us to delete one or more items in a list by using the `del` keyword.

**Example: `listopdemo2.py`**
```python
num = [1, 2, 3, 4, 5]
print(num)

del num[1]
print(num)

del num[1:3]
print(num)
```

**Output:**
```text
[1, 2, 3, 4, 5]
[1, 3, 4, 5]
[1, 5]
```

### Iterating a List
A list can be iterated by using a `for in` loop.

**Example: `listopdemo3.py`**
```python
lang = ['python', 'c', 'java', 'php']
print("The list items are \n")

for i in lang:
    print(i)
```

**Output:**
```text
The list items are 

python
c
java
php
```

---

## 5. List Functions & Methods
Python provides various in-built functions and methods which can be used with lists:
* `len()`
* `max()`
* `min()`
* `sum()`
* `list()`
* `sorted()`
* `append()`
* `remove()`
* `sort()`
* `reverse()`
* `count()`
* `index()`
* `insert()`
* `pop()`
* `clear()`

### len()
Used to find the length of the list (returns the number of items).
**Syntax:** `len(list)`
```python
num = [1, 2, 3, 4, 5, 6]
print("length of list :", len(num)) 
# Output: length of list : 6
```

### max()
Used to find the maximum value in the list.
**Syntax:** `max(list)`
```python
list1 = [1, 2, 3, 4, 5, 6]
list2 = ['java', 'c', 'python', 'cpp']
print("Max of list1 :", max(list1)) # Output: 6
print("Max of list2 :", max(list2)) # Output: python
```

### min()
Used to find the minimum value in the list.
**Syntax:** `min(list)`
```python
list1 = [1, 2, 3, 4, 5, 6]
list2 = ['java', 'c', 'python', 'cpp']
print("Min of list1 :", min(list1)) # Output: 1
print("Min of list2 :", min(list2)) # Output: c
```

### sum()
Returns the sum of all values in the list. List values must be numeric.
**Syntax:** `sum(list)`
```python
list1 = [1, 2, 3, 4, 5, 6]
print("Sum of list items:", sum(list1)) 
# Output: Sum of list items: 21
```

### list()
Used to convert a given sequence (like a string or tuple) into a list.
**Syntax:** `list(sequence)`
```python
str = "python"
list1 = list(str)
print(list1) 
# Output: ['p', 'y', 't', 'h', 'o', 'n']
```

### sorted()
Used to sort all items of a list in an ascending order without modifying the original list.
**Syntax:** `sorted(list)`
```python
num = [1, 3, 2, 4, 6, 5]
lang = ['java', 'c', 'python', 'cpp']
print(sorted(num))   # Output: [1, 2, 3, 4, 5, 6]
print(sorted(lang))  # Output: ['c', 'cpp', 'java', 'python']
```

### append()
Adds an item to the end of the list. The item may be a number, string, list, etc.
**Syntax:** `list.append(item)`
```python
num = [1, 2, 3, 4, 5]
lang = ['python', 'java']
num.append(6)
lang.append("cpp")
print(num)   # Output: [1, 2, 3, 4, 5, 6]
print(lang)  # Output: ['python', 'java', 'cpp']
```

### remove()
Removes the first occurrence of a specific item from the list. Throws a ValueError if the item is not present.
**Syntax:** `list.remove(item)`
```python
list1 = [1, 2, 3, 4, 5]
list2 = ['A', 'B', 'C', 'B', 'D']

list1.remove(2)
print(list1) # Output: [1, 3, 4, 5]

list2.remove("B")
print(list2) # Output: ['A', 'C', 'B', 'D']

list2.remove("E") # Output: ValueError: list.remove(x): x not in list
```

### sort()
Sorts the list elements in-place. By default, it sorts in ascending order. Use the optional `reverse=True` parameter to sort descending.
**Syntax:** `list.sort([reverse=True])`
```python
list1 = [6, 8, 2, 4, 10]
list1.sort()
print(list1) # Output: [2, 4, 6, 8, 10]

list1.sort(reverse=True)
print(list1) # Output: [10, 8, 6, 4, 2]
```

### reverse()
Reverses the elements of the list in-place (the last index value becomes the 0th index).
**Syntax:** `list.reverse()`
```python
list1 = [6, 8, 2, 4, 10]
list1.reverse()
print(list1) # Output: [10, 4, 2, 8, 6]
```

### count()
Returns the number of times a specified element appears in the list. Returns 0 if not present.
**Syntax:** `list.count(item)`
```python
num = [1, 2, 3, 4, 3, 2, 2, 1, 4, 5, 8]
print("Count of 2 is:", num.count(2))   # Output: 3
print("Count of 10 is:", num.count(10)) # Output: 0
```

### index()
Returns the index of the first occurrence of the passed element. Raises a ValueError if not present. Optional `start` and `end` parameters limit the search area.
**Syntax:** `list.index(item, [start, [end]])`
```python
list1 = ['p', 'y', 't', 'o', 'n', 'p']
print(list1.index('t'))       # Output: 2
print(list1.index('p'))       # Output: 0
print(list1.index('p', 1))    # Output: 5
print(list1.index('z'))       # Output: ValueError
```

### insert()
Inserts an element at a specified index. The first argument is the index before which to insert.
**Syntax:** `list.insert(index, item)`
```python
num = [10, 20, 30, 40, 50]
num.insert(4, 60)
print(num) # Output: [10, 20, 30, 40, 60, 50]

num.insert(7, 70)
print(num) # Output: [10, 20, 30, 40, 60, 50, 70]
```

### pop()
Removes and returns an element present at a specified index. If no index is specified, it removes and returns the last element.
**Syntax:** `list.pop([index])`
```python
num = [10, 20, 30, 40, 50]

num.pop()
print(num) # Output: [10, 20, 30, 40]

num.pop(2)
print(num) # Output: [10, 20, 40]

num.pop(7) # Output: IndexError: pop index out of range
```

### clear()
Removes all elements from the list, emptying it completely.
**Syntax:** `list.clear()`
```python
num = [10, 20, 30, 40, 50]
num.clear()
print(num) # Output: []
```