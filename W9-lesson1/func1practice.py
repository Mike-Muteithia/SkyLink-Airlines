# A function that calculates the grade of students

def student_grades(score):
  if (score <= 100 and score >= 91):
    return("A")
  elif (score <= 90 and score >= 81):
    return("B")
  elif (score <= 80 and score >= 71):
    return("C")
  elif (score <= 70 and score >= 61):
    return("D")
  elif (score <= 60 and score >= 51):
    return("E")
  elif (score <= 50 and score >= 0):
      return("F")
  else:
    return("invalid score")

print(student_grades(100))
print(student_grades(92))
print(student_grades(88))
print(student_grades(74))
print(student_grades(63))
print(student_grades(58))
print(student_grades(49))
print(student_grades(2))