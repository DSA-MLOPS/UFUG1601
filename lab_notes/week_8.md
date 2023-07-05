## Week 8 Lab: Basic File Handling

### Objective 

This lab aims to familiarize students with file handling in Python. Students will learn how to read from and write to text files, and will gain experience handling errors that might occur during these operations.

### Tasks

1. **Task 1: Reading from a File (30 minutes)** - In this task, students should demonstrate the ability to read from a text file. For example:

    * Open a provided text file in read mode.
    * Print each line of the file.

    Provide the following example to guide the students:

    ```python
    with open("example.txt", "r") as file:
        for line in file:
            print(line.strip())
    ```

2. **Task 2: Writing to a File (30 minutes)** - Students should practice writing to a text file. For example:

    * Open a new text file in write mode.
    * Write a few lines of text to the file.

    Provide the following example to guide the students:

    ```python
    with open("output.txt", "w") as file:
        file.write("Hello, world!\n")
        file.write("This is a new file.\n")
    ```

### Homework Assignment

As a homework assignment, students should write a more complex program that uses both reading and writing. They might, for instance, create a "note taking" program where the user can enter notes, and the notes are saved to a file. When the program is run, it could first print out all the notes that have been saved so far.

[**Tips** :bulb:] Thinking about experimenting with different ways of reading and writing files. They might try reading a large file one line at a time, or reading the entire file into a list of lines with the `readlines` method. They could also experiment with writing to a file one line at a time, or writing multiple lines at once with the `writelines` method.