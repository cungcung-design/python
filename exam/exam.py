# x = 5
# if x > 2:
#     print("Alpha")
# elif x < 4 or x == 5:
#     print("Beta")
# # qes 1: ans => Alpha


# a = [1, 2]
# b = [1, 2]
# print(a is b, a == b)
# # qes 2  ans => Flas True

# # bool False is   the number 0, and the value None. And the value False evaluates to False.


# score = 85
# if score > 90:
#      print("A")
# elif score > 80:
#      print("B")
# elif score > 70:
#     print("C")

## qes 4 : ans => B


# x = 10
# if x % 2 == 0:
#     print("Even")
# else:
#     print("Odd")

# # qes 5 is anser +> Even

# for i in range(3):
#     print(i, end="")

# # qes 6 ans is => 012

# i = 0
# while i < 3:
#     print("Hi")
#     i += 1

# # qes 7 ans is => Hi Hi Hi

# for i in range(1, 10, 4):
#     print(i, end="")
# # qes 8 ans is =>159

# for char in "cat":
#     if char == "a":
#         continue
#     print(char)
#     # qes 9 ans is =>ct

# nums = [1, 2]
# for n in nums:
#     nums.append(n)
#     break
# print(nums)
# # qes 10 ans is =>[1,2,1]


# def func(a, b=2):
#     return a + b


# print(func(5))
# # qes 11 ans is =>7


# def multiply(*args):
#     res = 1
#     for nn in args:
#         res *= n
#         return res


# print(multiply(2, 3, 4))
# # qes 12 ans is =>1


# def outer():

#     def inner():
#         return "hello"

#     return inner


# print(outer()())
# # qes 13 ans is => hello


# class A:
#     def __init__(self, x):
#         self.x = x
#         obj = A(10)
#         print(obj.x)


# # qes 14 ans is => no ouput return


# class counter:
#     count = 0

#     def __init__(self):
#         counter.count += 1
#         c1 = counter()
#         c2 = counter()
#         print(counter.count)


# # qes 15 ans is => no ouput return

# class Person:
#     def __init__(self,name):
#         self.name = name
#         p = Person("John")
#         del p.name
#         print (p.name)
 # qes 16 ans is => no ouput return
       

# numbers = [1,2,3,4,5]
# total  = 0
# for i in numbers:
#  if i % 2 ==0:
#      total = i
#      print (total)
    
# qes 17 ans is  => 2  4

# numbers= [ 1,2,3,4,5]
# for i in numbers: 
#   if i % 2 ==0:
#       numbers.remove(i)
#       print (numbers)

# qes 18 ans is  => [1, 3, 4, 5] [1, 3, 5]
# when we chnage i % 2! = 0 ,

 
numbers = [1, 2, 3, 4, 5]
i = numbers
for i in numbers:
    if i % 2 != 0:
        numbers.remove(i)
        print(i)
# qes 18 ans is  => 1 3 5

# when i wite the code like that numbers = [1, 2, 3, 4, 5]
# i = numbers
# for i in numbers:
#     if i % 2 != 0:
#         numbers.remove(i)
#         print(i)

# it remove all the even numbers form the list