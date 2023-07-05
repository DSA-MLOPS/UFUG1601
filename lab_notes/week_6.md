## Week 6 Lab: Functions and Modularization in Python

### Objective

The aim of this lab is to give students experience in defining their own functions, understanding the concept of function scope, and modularizing their code. They'll practice using both pre-defined and user-defined functions in Python.

### Tasks

1. **Task 1: Defining and Calling Functions (20 minutes)** - In this task, students should demonstrate the ability to create and use their own functions. For example:

* Define a function `greet` that takes a name as an argument and prints a greeting to that person.
* Call your `greet` function with a few different names to test it.

Provide the following example to guide the students:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
greet("Bob")
greet("Charlie")
```

2. **Task 2: Function Scope (20 minutes)** - Students should practice understanding function scope. For example:

* Define a function that tries to modify a global variable.
* Show that the global variable is not changed after the function call.

Provide the following example to guide the students:

```python
x = 10

def modify_x():
    x = 5
    print(f"x inside function: {x}")

modify_x()
print(f"x outside function: {x}")
```

3. **Task 3: Code Modularization (20 minutes)** - Students should learn how to organize their code into functions for better readability and reusability.

* Take a piece of code they wrote for a previous task and break it down into functions.
* Each function should do one specific thing.

Discuss with students about their previous codes and guide them on how to modularize it.

### Homework Assignment

As a homework assignment, students should write a more complex program that consists of multiple functions. They could, for instance, expand their "database" program from the previous homework assignment to include functions for saving the database to a file and loading it from a file.

[**Tips** :bulb:] Thinking about how breaking code down into functions makes it easier to understand and maintain. This will be especially important as you start to work on larger and more complex programs.