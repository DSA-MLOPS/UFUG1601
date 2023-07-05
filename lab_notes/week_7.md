## Week 7 Lab: Basic Object Concepts - Classes and Objects

### Objective

The aim of this lab is to introduce students to object-oriented programming (OOP) in Python. They will learn how to define classes, create objects, and use instance methods and variables.

### Tasks

1. **Task 1: Defining Classes and Creating Objects (30 minutes)** - In this task, students should demonstrate the ability to define a class and create an object of that class. For example:

    * Define a `Car` class with `make`, `model`, and `year` attributes and a `describe` method.
    * Create a few `Car` objects and call their `describe` methods.

    Provide the following example to guide the students:

    ```python
    class Car:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year
        
        def describe(self):
            print(f"This is a {self.year} {self.make} {self.model}")

    my_car = Car("Toyota", "Corolla", 2020)
    my_car.describe()

    your_car = Car("Honda", "Civic", 2021)
    your_car.describe()
    ```
2. **Task 2: Instance Variables and Methods (30 minutes)** - Students should practice using instance variables and methods. For example:

    * Add a `mileage` attribute and a `drive` method to the `Car` class.
    * Use the `drive` method to increase the `mileage` of a `Car` object.

    Provide the following example to guide the students:

    ```python
    class Car:
        def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year
            self.mileage = 0
        
        def describe(self):
            print(f"This is a {self.year} {self.make} {self.model} with {self.mileage} miles")
        
        def drive(self, miles):
            self.mileage += miles

    my_car = Car("Toyota", "Corolla", 2020)
    my_car.drive(100)
    my_car.describe()
    ```

### Homework Assignment

As a homework assignment, students should write a program that uses multiple classes. They might, for instance, create a `Garage` class that contains a list of `Car` objects. They could then write methods for the `Garage` class to add and remove cars, and to print information about all the cars in the garage.

[**Tips** :bulb:] Thinking about how organizing code into classes and objects can make it easier to structure and understand. This is a fundamental concept in many types of programming, not just Python, and it's a good one to get comfortable with.