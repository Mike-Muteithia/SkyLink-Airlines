a = int(input("Enter a value: "))
b = int(input("Enter b value: "))
c = int(input("Enter c value: "))

if (a>b) and (a>c):
  print("Maximum vaule is :", a)
elif (b>a) and (b>c):
  print("Maximum value is :", b)
else: 
  print("Maximum value is :", c)
