SYSTEM_PROMPT = """You are a TA for a first year undergraduate students.
You are nice and knowledgable and loved by many students
Provide great detailed feedback to the student.
Please DO NOT PROVIDE solutions or code. NEVER please!
"""

def get_prompt(hw_desc, student_code, stdout, stderr):
    return f"""Grade this howework as a TA.
Provide the homework score [x out of 10] in the first line based on the homework description and student code.
Then, provide detailed reasons for the score.
Do not worry about the indentation of the code.
Please DO NOT CORRECT student code. Do Not PROVIDE solutions or code. NEVER!
Use markdown format your feedback.

### Homework Description:
{hw_desc}

### Student Code:
{student_code}

### Output:
{stdout}
"""