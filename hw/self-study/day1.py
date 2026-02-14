# name = " cung"
# print(name)
# x, y ,z = "orange", "banana", "apple"
# print(x)
# print(y)
# print(z)

# x = y = z = "apple"
# print(x)
# print(y)
# print(z)

# fruits = ["apple", "banana", "cherry"]
# x, y ,z = fruits
# print(x)
# print(y)
# print(z)


# x = "python"
# y = 'is'
# z = "awesome"
# print(x+y+z)

# x = 5
# y = "john"
# print (x,y)

# x = "awesome"


# def myfunc():
#     x = "fantastic"
#     print("python is " + x)


# myfunc()

# x = int (1)
# y = int (2.8)
# z = int("3")
# print(x)
# print(y)
# print(z)

# print("It's alright")
# print("He is called 'Johnny'")
# print('He is called "Johnny"')

# a = """Lorem ipsum dolor sit amet,
# consectetur adipiscing elit,
# sed do eiusmod tempor incididunt
# ut labore et dolore magna aliqua."""
# print(a)

# b = "Hello, World!"
# print(b[2:])

# a = " Hello, World!    "
# print(a.strip())


# a = "Hello"
# b = "World"
# c = a +"" + b
# print(c)

# age = 18
# txt = f"My name is John, and I am {age}"
# print(txt)

# price = 5000
# shirt = f" this shirt is about : {price* 20}"
# print(shirt)

# txt = "We are the so-called \"Vikings\" from the north."
# print(txt)

# x = 15
# y = 4


# print(x + y)
# print(x - y)
# print(x * y)
# print(x / y)
# print(x % y)
# print(x ** y)
# print(x // y)

# x = 5
# y = 3

# print(x == y)
# print(x != y)
# print(x > y)
# print(x < y)
# print(x >= y)
# print(x <= y)
# x = 5

# print(1 < x < 10)

# print(1 < x and x < 10)




# thislist = ["apple", "banana", "cherry"]
# thislist.insert(1, "orange")
# print(thislist)

# thisdic = {
#     "brand": "Ford",
#     "model": "Mustang",
#     "year": 1964,
#     "colors" : ["red", "white", "blue"]
# }

# for x in thisdic.values():
#     print(x)

# scores = 101
# if scores >= 90:
#     print("Grade A")
# elif scores >= 80:
#     print("Grade B")
# elif scores >= 70:
#     print("Grade C")
# elif scores >= 60:
#     print("Grade D")
# else:
#     print("Fail")
    
# day = 4
# if day == 1 :
#     print("Monday")
# elif day == 2 :
#     print("Tuesday")
# elif day == 3 :
#     print("Wednesday")
# elif day == 4 :
#     print("Thursday")
# elif day == 5 :
#     print("Friday")
# elif day == 6 :
#     print("Saturday")
# elif day == 7 :
#     print("Sunday")
    
# a = 200
# b = 100
# c = 300
# if a > b  and   c > a:
#     print("both are ture")

# age = 25
# has_license = True
# if age >= 18:
#  if has_license:
#     print("Eligible to drive")
# else:
#     print("Not eligible to drive")


# i = 1 
# while i <= 6:
#      print(i)
#      i += 1
     
# i = 1 
# while i < 6:
#     print(i)
#     if i == 3:
#         break
#     i +=1
    

# i = 0 
# while i < 6:
#     i += 1
#     if i == 3:
#         continue
#     print(i)
    
# fruits = ["apple", "banana", "cherry"]
# for x in fruits:
#     print(x)
#     if x == "banana":
#         continue
    
# for i in range(2):
#     for j in range(3):
#         print(i, j)

#     print(i)
# def my_function():
#   print("Hello from a function")

# my_function()

# def my_generator():
#   yield 1
#   yield 2
#   yield 3

# for value in my_generator():
#   print(value)
  
# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
# p1 = Person("John", 36)
# print(p1.name)
# print(p1.age)

# Student Management System

class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Grade: {self.grade}")

    def update_grade(self, new_grade):
        self.grade = new_grade
        print(f"{self.name}'s grade updated to {self.grade}")


# Main program
students = []

# Adding students
students.append(Student("Alex", 20, "A"))
students.append(Student("Mg Mg", 15, "B"))

# Display all students
print("All Students:")
for s in students:
    s.display_info()

# Update a student's grade
students[1].update_grade("A+")

# Display after update
print("\nAfter Update:")
for s in students:
    s.display_info()


# Library Book Management System

class Book:
    def __init__(self, title, author, status="Available"):
        self.title = title
        self.author = author
        self.status = status  # Available / Borrowed

    def display_info(self):
        print(f"Title: {self.title}, Author: {self.author}, Status: {self.status}")

    def borrow_book(self):
        if self.status == "Available":
            self.status = "Borrowed"
            print(f"{self.title} has been borrowed.")
        else:
            print(f"Sorry, {self.title} is already borrowed.")

    def return_book(self):
        if self.status == "Borrowed":
            self.status = "Available"
            print(f"{self.title} has been returned.")
        else:
            print(f"{self.title} is already available.")


# Library list
library = []

# Function to add books
def add_book(title, author):
    library.append(Book(title, author))
    print(f"{title} added to the library.")

# Function to display all books
def display_books():
    print("\nLibrary Books:")
    for b in library:
        b.display_info()

# Function to search a book by title
def search_book(title):
    for b in library:
        if b.title.lower() == title.lower():
            return b
    return None


# === Main Program ===
while True:
    print("\n--- Library Menu ---")
    print("1. Add Book")
    print("2. Display Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Exit")

    choice = input("Enter choice (1-5): ")

    if choice == "1":
        t = input("Book Title: ")
        a = input("Author: ")
        add_book(t, a)

    elif choice == "2":
        display_books()

    elif choice == "3":
        t = input("Enter title to borrow: ")
        book = search_book(t)
        if book:
            book.borrow_book()
        else:
            print("Book not found!")

    elif choice == "4":
        t = input("Enter title to return: ")
        book = search_book(t)
        if book:
            book.return_book()
        else:
            print("Book not found!")

    elif choice == "5":
        print("Exiting Library System. Goodbye!")
        break

    else:
        print("Invalid choice! Please enter 1-5.")
