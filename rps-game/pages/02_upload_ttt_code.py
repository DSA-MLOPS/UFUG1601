import streamlit as st
from streamlit_ace import st_ace
from code_util import execute_code
from db_util import db_execute_query, db_select_query


st.title("Upload Student Code")
st.write("Please enter your student ID and Python code with the rps() function below.")

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
)

if st.button("Upload Code") and student_code and student_id:
    test_output, error = execute_code(student_code)
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
