
# add_lambda = lambda a,b: a+b
# print(add_lambda(2,5))

# calculate  = lambda x,y: (x + y ) - (x  - y)
# result = calculate (10,5)
# print (result)

# ages = [10, 15, 17, 18, 22, 68, 47]

# def myfunc(x):
#     if x < 18:
#         return False
#     else:
#         return True

# adults = filter(myfunc, ages)
# for i in adults:
#     print (i)
# print(list(adults))
# names = ["magmg", "kyaw kyaw", "mya mya"]

# uppercaseName = list(map(str.upper, names))
# print(list(uppercaseName))


# numbers = [1,2,3,4,5]
# squared = map(lambda x : x * 2 , numbers)
# print(list(squared))

# names = ["kyaw "," mg", "alice", " bob" , " hh" , " eee"]
# filter_named = filter (lambda name : len (name) > 8 ,names)
# print(list(filter_named))     homework

# modifiedNumbers = [1,2,3,4,5]
# numbers = list(map(lambda x : x * x + 10, modifiedNumbers))
# print(numbers)

# grades = [ 80,17,75,99]
# results = list(map(lambda score :  ' pass ' if score >= 80 else  'fail', grades))
# print(results)


# try:
#     n = 1000
#     res = 100/n
# except ZeroDivisionError:
#     print ( "you can;t deivede by zero")
# except ValueError:
#     print ("Enter a valid number")
# else:
#     print ("result is ", res)
# finally : 
#     print ("execution completed")


dataList = [5,10,"A ",25,0,50,-1]
def prodatorErHandling  (dataList):
    processCount = 0
    for item in dataList:
        try:
            number = int (item)
            if number > 0:
                result = number * 2
                print ("success", number , "result" ,result)
            elif number == 0:
                print("nit process and skip")
            else : 
                print("do not acceept navgiv value", number)
        except (ValueError,TypeError) as e:
             print ( "error", item)
             continue
        except Exception as e : 
             print ('Unknown error',e)
             break
        print ("finally aarrage success number", processCount)
    
prodatorErHandling(dataList)