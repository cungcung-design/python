# name = "kyaw kyaw"
# city = "yangon"
# age = 20
# score = 20
# score = 25
# a = 5
# b = 10
# c = a + b
# y = 2 + 1j
# x = list (("apple,mango,orange"))
# tuple =("flutter","mernstak","python")
# number = ["10","20","30"]


# student = {
#     name: "Alex",
#     age: 18,
#     "city": "Yangon"
# }
# print (student.get("city"))

# mark = 40
# if(mark >= 80 ) :
#       print("grade A")
# elif (mark >= 60):
#       print("Grade B")
# else : 
#       print ("Fail")

# age = 35
# if age<=12:
#   print("Child")
# elif age<=16:
#     print("teenager")
# elif age<=35:
#       print ("yound adult")
# else:
#     print ("adult")
    
    
# age = 70
# is_member = False
# if age >= 60:
#   if is_member:
#     print("30% Discount")
#   else:
#     print("20% Discount")
    
# number = 4

# match number:
#     case 1:
#         print("one")
#     case 2 | 3:
#         print("two or three")
#     case _:
#         print("other number")


# for i in range (10):
#     print(i)
    
# for i in range (4,15):
#      print(i)   
     
# for i in range (10,0,-2):
#      print(i)
     
# numbers = list(range(3,8))
# print (numbers)

# for i in "Web Design and Development":
#     if i == "e" or i == "d":
#      break
#     print (i)

# numbers = [1,2,3,4,5,6,7,8,9,10,11,12]
# target_num = 7

# for num in numbers:
#     print("number are",num)
#     if num == target_num:
#         break
#     print("number is", num)

# for  i in range (1,7):
#     print (i)
# else:
#     print("for over 7 loopinf")
    
# items = ["apple", "banana", "orange"]

# for a, b in enumerate(items):
#     print(a, b)

# numbers = [1,2,3,4,5,6,7]
# for i,j in enumerate (numbers):
#         if j % 2 == 0:
#             continue
#         print(i,j)
        
# for i in range (1,5):
#     for j in range (1,5):
#       if i == j:
#         continue
#     print(i,j)


# number = 6
# max_num = 10

# for i in range(number, number + 1):
#     for j in range(1, max_num + 1):
#         if j == 9 or j == 12:
#             continue
#         result = i * j
#         print(i, "x", j, "=", result)

# count = 1
# while count < 5:
#     print("this is while loop sample", count)
#     count = count +1
#     print ("complete")
    
  
# friuts = ["apple","mango", "orange"]
# index =2
# while index <len(friuts):
#       current = friuts[index]
#       print (current)
#       index +=1


# for i in range(1, 8):
#     print(i)

# fruits = ["apple", "banana", "mango"]

# for fruit in fruits:
#       print(fruit)
      
# for i in range(1, 11):
#     if i % 2 == 0:
#         print(i, "is even")
#     else:
#         print(i, "is odd")

# def add(a, b):
#     return a + b

# result = add(10, 5)
# print(result)

# x = abs(3+5j)
# print(x)

def show():
    print("Hello")

def give():
    return "Hello"

show()        # prints Hello
x = give()    # stores Hello
print(x)
