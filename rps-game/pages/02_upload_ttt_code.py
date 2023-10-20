import streamlit as st
from streamlit_ace import st_ace
from code_util import execute_code
from db_util import db_execute_query, db_select_query


st.title("Upload Student Code")
st.write("Please enter your student ID and next_move(board) that returns x, y function below.")

student_id = st.text_input("Student ID:")
# student_code = st.text_area("Write program that prints out 'rock', 'scissors', or 'paper'")

# student_id = st.text_input("Student ID:")
# student_code = st.text_area("Write Code:", height=300)
# Spawn a new Ace editor
student_code = st_ace(
    auto_update=True,
    height=300,
    language="python",
    keybinding="vscode",
    show_gutter=True,
    placeholder="Write your python code here...",
    value="""### we will pass board (3x3 list)
# 0: nothing
# 1: X (letter X)
# 2: Y (letter Y)
#
# You need to return x, y

def next_move(board):\n
    return 0, 0
"""
)

basic_code = """
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
x, y = next_move(board)

assert x >= 0 and x <= 2
assert y >= 0 and y <= 2
"""

if st.button("Upload Code"):
    if not student_id:
        st.error("Student ID cannot be empty.")
        st.stop()
    if not student_code:
        st.error("Student code cannot be empty.")
        st.stop()
    test_output, error = execute_code(student_code + basic_code)
    if error:
        st.error(f"Code execution failed: {error}")
    elif test_output is not None:
        st.success(f"Code execution successful: {test_output}")
        row = db_select_query('SELECT * FROM students WHERE student_id=?', (student_id,))
        if row is None:
            db_execute_query("INSERT INTO students VALUES (?, ?, 0)", (student_id, student_code))
            st.success("Code uploaded successfully!")
        else:
            db_execute_query("UPDATE students SET code = ? WHERE student_id = ?", (student_code, student_id))
            st.success("Code updated successfully!")
    else:
        st.error("Code execution failed. Please check your code.")
