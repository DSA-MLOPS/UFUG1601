import streamlit as st
from db_util import c, conn
from code_util import execute_code
from gpt_util import gpt_grade

HW_DESCRIPTION = """
Write code to print out the followings:
*
**
***
****
***
**
*

Please use while loop to solve this problem.
"""

st.title("HW Submission")
st.write("Please enter your student ID and homework code.")


st.markdown(f"```{HW_DESCRIPTION}```")

student_id = st.text_input("Student ID:")
student_code = st.text_area("Code:")

if st.button("Upload Code"):
    if student_id and student_code:
        test_output, error = execute_code(student_code)
        if error:
            st.error(f"Code execution failed: {error}")
        elif test_output is not None:
            st.success(f"Code execution successful: {test_output}")
            st.write("Wait for a few seconds for the auto feedback.")
            gpt_comments = gpt_grade(HW_DESCRIPTION, student_code, test_output, error)
            st.markdown(gpt_comments)
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
