# def Greeting ():
#   print("hello welcome to python")

# Greeting()

# def number (x: int):
#    if (x%2==0):
    
#      print("even") 
#    else:
#      return ("odd")

# print("number(15)")


# def login(username, password):
#     correctname = "admin"
#     correctpassword = "admin123"
    
#     if correctname == username and correctpassword == password:
#         print("Login successful")
#         return True
#     else:
#         print("Login failed")
#         return False

# login("admin", "admin123")


# def number(num1, num2, num3):
#     total = num1 + num2 + num3
#     print("Total number is:", total)

#     numbers = [num1, num2, num3]

#     for i, num in enumerate(numbers,1):
#         if num % 2 == 0:
#             print(num, i, "is even")
#         else:
#             print(num, i, "is odd")

#     largest = max(numbers)
#     smallest = min(numbers)

#     print("largest number is:", largest)
#     print("smallest number is:", smallest)

# number(10, 11, 20)
   
  
# def find_max(x, y, z):
#     numbers = [x, y, z]
#     largest = max(numbers)
#     print(largest)
# find_max(1,2,3)

def find_max(numberList):
    max_num = numberList[0]
    for num in numberList:
        if num > max_num:
            max_num = num
    return max_num  

print(find_max([1, 2, 4, 10]))
