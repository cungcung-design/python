print(abs(-10))
print(abs(5))
# returns the absolute value of a number


values = [True, True, True]
print(all(values))
# checks whether all elements are ture or false

zip()
names = ["Aung", "Kyaw"]
ages = [20, 18]
classes = ["Grade A", "Grade B"]
for name, age, cls in zip(names, ages, classes):
    print(f"Name: {name}, Age: {age}, Class: {cls}")
# combines multiple together item by item.


nums = [5, 2, 9, 1]
print(sorted(nums))
# returns a new sorted list without changing the original.

text = ["a", "b", "c"]
for txt in reversed(text):
    print(txt)
# returns items in reverse order.

numbers = bytes([1, 2, 3, 4])
view = memoryview(numbers)
print(view[0])
# memoryview() lets you access memory data without copying it.

nums = [1, 2, 2, 3, 3, 4]
print(set(nums))
# set() removes duplicate values.

student = dict(name="Aung", age=18)
print(student)
# dict() creates a dictionary key-value pair.

x = 10
print(isinstance(x, int))
print(isinstance(x, str))
# isinstance() checks if an object belongs to a specific type.


a = divmod(15, 5)
print(a)
# division and returns both quotient and remainder .
