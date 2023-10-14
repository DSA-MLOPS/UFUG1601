import streamlit as st
import json
from PIL import Image
from code_util import execute_code
from solar import solar_grade
from gpt_util import gpt_grade
from hw_parser import get_head_contents
from streamlit_ace import st_ace
import qrcode
import io
import os

# Get team code
get_query_params = st.experimental_get_query_params()
space = get_query_params.get("space", ["hw"])[0]

md_file = f"{space}.md"
if not os.path.exists(md_file):
    st.error(f"Team {space} not found!")
    st.stop()

hw_dict = get_head_contents(md_file)
hw_keys = ["Home"] + list(hw_dict.keys())
page = st.sidebar.selectbox("Select a quiz:", hw_keys)


# Home Display for student QR code
if page == "Home":
    st.title(f"AI-TA Page: {space}")
    st.write("Welcome to the AI-TA platform!")
    qr_img = qrcode.make("https://https://ta.sung.devstage.ai/space={space}")

    # Convert the QR code to bytes
    img_bytes = io.BytesIO()
    qr_img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()  # Get the bytes value from BytesIO object
    st.image(img_bytes, caption="QR Code for AI-TA platform!", use_column_width=True)
elif page in hw_keys:
    st.title(page)
    hw_desc = hw_dict[page]["description"]
    st.markdown(hw_desc)

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

    if st.button("Consult AI-TA") and student_code:
        test_output, error = execute_code(student_code)
        student_code = ""
        if error:
            st.error(f"Code execution failed: {error}")
        elif test_output is not None:
            st.success("Code execution successful:")
            st.text(test_output)
            st.info("⏳ Checking your code with AI-TA (SOLAR)...")
            solar_res_box = st.empty()
            ta_comments = solar_grade(hw_desc, student_code, test_output, error, solar_res_box.markdown)
            # st.markdown(ta_comments)

            st.info("⏳ Checking your code with AI-TA (GPT)...")
            gpt_res_box = st.empty()
            ta_comments = gpt_grade(hw_desc, student_code, test_output, error, gpt_res_box.markdown)
            # st.markdown(ta_comments)

            st.success("🎉 AI-TA finished grading your code!")
        else:
            st.error("Code execution failed. Please check your code.")
