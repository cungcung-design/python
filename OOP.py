
# class cat:
#     sound = "bark"
    
# tommy = cat()
# print(tommy.sound)
# class Person:
#     def greet(self):
#         print("Hello!")
# p1 = Person()
# p1.greet()


# class calculation:
#     def sum (datalist):
#         if not datalist:
#             return 0
#         return sum(datalist)/ len(datalist)
# dataSample = [10,20,30]
# advarged = calculation.sum(dataSample)
# print("value numbrer of advagte", advarged)

# class People:
#     job_type = "manager" 

#     def __init__(self, name, age):
#         self.name = name  
#         self.age = age 

# mgmg = People("kyaw kyaw", 18)

# print(mgmg.name)
# print(mgmg.age)
# print(mgmg.job_type)

# class person:
#     def speak (self):
#      print("I can speak burmese")
     
    
# class Car:
#     wheel = 4  # Class variable

#     def __init__(self, model, brand):
#         self.model = model 
#         self.brand = brand

#     def display_info(self): 
#         print(f"This car is a {self.brand} {self.model} with {self.wheel} .")

# car1 = Car("civic", "Honda")
# car2 = Car("Model 3", "Tesla")

# print(car1.brand)
# print(car2.model)
# car1.display_info()
# car2.display_info()


# class Animal:
#     def __init__(self, name):
#         self.name = name 

#     def eat(self):
#         return f"This {self.name} is eating."

# class Cat(Animal):
#     def meow(self):
#         return f"{self.name} says: Meow"
#     def eat(self):
#         return f"this cat {self.name} is eating like a dog"

# my_cat = Cat("Bubu")

# print(my_cat.eat()) 
# print(my_cat.meow())


# class Doctor:
#     def work (self):
#         return " treantmetn the patience"
# class teacher :
#     def work(self):
#         return" teaching the student"
    
# doctor = Doctor()
# teachers = teacher()
# print(doctor.work())
# print(teachers.work())


# class Animal:
#     def sound(self):
#         return "This sound is loud"

# class Cat(Animal):
#     def sound(self):
#         return "This sound is meow"

# class Dog(Animal):
#     def sound(self):
#         return "This sound is woof woof"   
# my_cat = Cat()
# my_dog = Dog()

# my_animals = [my_cat, my_dog]

# for animal in my_animals:
#     print(animal.sound())
    
# class rectangle:
#     def __init__(self,width,height):
#         self.width = width
#         self.height = height
       
#     def area (self):
#         return self.width * self.height
  
# class radious:
#      def __init__(self, width):
#          self.width = width
         
#      def area (self):
#          return 3.14 * self.width
     
         
         
# mycall = [rectangle(5,4),radious(3)]
# for mycalls in mycall:
#     print(f"area: {mycalls.area()}")
    
    
# class employee:
#     def __init__(self,name,salary):
#         self.name = name 
#         self._salary = salary 
        
# emp = employee("kyaw", 60000)
# print(emp.name)
# print(emp._salary)


# class simplelight :
#     def __init__(self, initial_State):
#         self.__isOn = initial_State
#     def display_sate (self):
#         return f"{"ligght is on " if self.__isOn else  'light is off'}"
    
# buld = simplelight (initial_State= False)
# print (buld.display_sate())

# buld.__isOn = True
# print(buld.display_sate())


class Smartphone:
    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price

    def display_info(self):
        return f"This phone is {self.brand} {self.model} and price is {self.price}"

    def display_discount(self, price):
        discount_amount = self.price * (price / 100)
        self.price = self.price - discount_amount
        return f"Discount is: {price}"
    
    
my_phone = Smartphone("iPhone", "15", 1000)

print(my_phone.display_info())
print(my_phone.display_discount(10))
print(my_phone.display_info())
