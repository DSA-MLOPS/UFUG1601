## Week 4 Lab: Looping in Python - For Loop, Break, and Continue

### Objective

This lab focuses on understanding and implementing For loops and the use of Break and Continue statements in Python. Students will write programs that repeat tasks a set number of times, and control the flow of these tasks with Break and Continue.

### Tasks

1. **Task 1: For Loop (20 minutes) ** - In this task, students should write a program that uses a for loop to perform a task a certain number of times. For example: 

    * Write a program that iterates over a list of names and prints each one.

    Provide the following example to guide the students:

    ```python
    names = ["Alice", "Bob", "Charlie", "Dave"]
    for name in names:
        print(name)
    ```

2. **Task 2: Break Statement (20 minutes) ** - Students should write a program that uses the break statement to exit a loop prematurely. For example:

    * Write a program that iterates over a list of numbers and stops as soon as it encounters a number greater than 10.

    Provide the following example to guide the students:

    ```python
    numbers = [1, 3, 5, 7, 11, 13, 17]
    for num in numbers:
        if num > 10:
            break
        print(num)
    ```

3. **Task 3: Continue Statement (20 minutes)** - Students should write a program that uses the continue statement to skip an iteration in a loop. For example:

    * Write a program that iterates over a list of numbers and skips any negative numbers, only printing the positive ones.

    Provide the following example to guide the students:
    ```python
    numbers = [1, -3, 5, -7, 11, -13, 17]
    for num in numbers:
        if num < 0:
            continue
        print(num)
    ```

### Homework Assignment

As a homework assignment, students should be asked to write a program that uses all of the concepts covered in this lab. They might create a program that asks the user to guess a number between 1 and 100, and uses a for loop to limit the number of guesses to 10. The break statement can be used to exit the loop once the user guesses correctly, and the continue statement can be used to skip an iteration if the user inputs something that's not a number.

[**Tips** :bulb:] Thinking about where these looping concepts might be used in real programming situations.