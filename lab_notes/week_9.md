## Week 9 Lab: Review and Advanced Topics

### Objective

The purpose of this lab is to review the Python concepts learned so far and to introduce some advanced topics. The students will work on a capstone project that combines all the knowledge and skills they've gained over the course.

### Tasks

1. **Task 1: Capstone Project (90 minutes)** - Students will be tasked with building a "Virtual Library System". This system should:

    * Have a `Library` class that contains a list of `Book` objects (each `Book` should have properties like `title`, `author`, `pages`, and `current_page`).
    * Users should be able to `add` and `remove` books from the Library.
    * Users should be able to `open` a book, which will print out the current page of the book.
    * Users should be able to `turn` the page of a book, which will update the `current_page` of the book and print it out.
    * The state of the Library should be saved to a file when the program ends, and loaded from a file when the program starts.

    Guide students to approach this project incrementally. They should first focus on implementing the `Book` class, then the `Library` class, and finally the saving and loading functionality.

### Homework Assignment

Students should complete any unfinished parts of the capstone project as homework. If they finish the capstone project, they could add extra features to it. For instance, they could add a `bookmark` to the `Book` class, or they could allow for multiple `Library` objects, each with a different name and saved to a different file.