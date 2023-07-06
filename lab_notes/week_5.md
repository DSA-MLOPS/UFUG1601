## Week 5 Lab: Data Structures in Python - Lists and Dictionaries

### Objective

This lab aims to familiarize students with the use and manipulation of Lists and Dictionaries in Python. Students will create, modify, and query these data structures.

### Tasks

1. **Task 1: Lists (20 minutes)** - In this task, students should demonstrate the ability to create and manipulate lists. For example:

    * Create a list of your five favorite foods.
    * Add another food to the end of the list.
    * Remove the second food from the list.
    * Print the list to confirm your changes.

    Provide the following example to guide the students:

    ```python
    foods = ["pizza", "pasta", "burger", "sushi", "steak"]
    foods.append("ice cream")
    del foods[1]
    print(foods)
    ```

2. **Task 2: Dictionaries (20 minutes)** - Students should demonstrate the ability to create and manipulate dictionaries. For example:

    * Create a dictionary where the keys are names of your friends and the values are their favorite colors.
    * Add a new key-value pair to the dictionary.
    * Change the favorite color of one of your friends.
    * Print the dictionary to confirm your changes.

    Provide the following example to guide the students:

    ```python
    friends_colors = {"Alice": "blue", "Bob": "green", "Charlie": "red"}
    friends_colors["Dave"] = "purple"
    friends_colors["Alice"] = "pink"
    print(friends_colors)
    ```


### Homework Assignment

As a homework assignment, students should be asked to create a more complex program using lists and dictionaries. They could create a simple "database" of people, where each person is represented as a dictionary with keys like "name", "age", and "favorite color", and all of these dictionaries are stored in a list. Students could then write functions to add a person to the database, remove a person from the database, or search for people based on various criteria.

[**Tips** :bulb:] Thinking about how to experiment with different list and dictionary methods and to think about real-world applications of these data structures. Data structures are a fundamental part of programming, and there are many possibilities for creative exploration here.