import streamlit as st
from db_util import c, conn
from code_util import execute_code

st.title("Upload Student Code")
st.write("Please enter your student ID and Python code with the rps() function below.")

student_id = st.text_input("Student ID:")
student_code = st.text_area("Write program that prints out 'rock', 'scissors', or 'paper'")

if st.button("Upload Code"):
    if student_id and student_code:
        test_output, error = execute_code(student_code)
        if error:
            st.error(f"Code execution failed: {error}")
        elif test_output is not None:
            st.success(f"Code execution successful: {test_output}")
            c.execute('SELECT * FROM students WHERE student_id=?', (student_id,))
            row = c.fetchone()
            if row is None:
                c.execute("INSERT INTO students VALUES (?, ?, 0)", (student_id, student_code))
                conn.commit()
                st.success("Code uploaded successfully!")
            else:
                c.execute("UPDATE students SET code = ? WHERE student_id = ?", (student_code, student_id))
                conn.commit()
                st.success("Code updated successfully!")
        else:
            st.error("Code execution failed. Please check your code.")
