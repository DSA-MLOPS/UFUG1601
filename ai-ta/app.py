import streamlit as st
import json
from PIL import Image
from code_util import execute_code
from solar import solar_grade
from gpt_util import gpt_grade, gpt_mk_quiz
from hw_parser import get_head_contents
from streamlit_ace import st_ace
import qrcode
import io
import os

MISTRAL_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
QWEN_MODEL = "togethercomputer/Qwen-7B-Chat"
DEFAULT_SPACE = "UFUG1601"
DEFAULT_URL = "https://ta.sung.devstage.ai/"
FEELING_LUCKY = "🍀 Feeling Lucky!"
SEPERATOR_MENU = "--------"
HOME_MENU = "Home"

# Get team code
get_query_params = st.experimental_get_query_params()
space = get_query_params.get("space", [DEFAULT_SPACE])[0]

md_file = f"{space}.md"
if not os.path.exists(md_file):
    st.error(f"Space {space} not found!")
    st.stop()

hw_dict = get_head_contents(md_file)
hw_keys = [HOME_MENU] + list(hw_dict.keys()) + [SEPERATOR_MENU, FEELING_LUCKY]
page = st.sidebar.selectbox("Select a quiz:", hw_keys)


# Home Display for student QR code
if page in [HOME_MENU, SEPERATOR_MENU]:
    st.title(f"AI-TA Page: {space}")
    st.write("Welcome to the AI-TA platform!")
    qr_img = qrcode.make(f"{DEFAULT_URL}?space={space}")

    # Convert the QR code to bytes
    img_bytes = io.BytesIO()
    qr_img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()  # Get the bytes value from BytesIO object
    st.image(img_bytes, caption="QR Code for AI-TA platform!", use_column_width=True)
elif page in hw_keys + [FEELING_LUCKY]:
    hw_desc_box = st.empty()
    if page == FEELING_LUCKY:
        hw_desc = gpt_mk_quiz(call_back_func=hw_desc_box.markdown)
        # Add button revisit this page
        st.sidebar.button("Give me another quiz!")
    else:
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

    if st.button("Ask AI for Feedback") and student_code:
        test_output, error = execute_code(student_code)
        if error:
            st.error(f"Code execution failed: {error}")
        elif test_output is not None:
            st.success("Code execution successful:")
            st.code(test_output, language="shellSession")
            
            with st.spinner("⏳ Checking your code with AI-TA (SOLAR)..."):
                st.info("💬 Commmments and Grade from SOLAR AI-TA:")
                solar_res_box = st.empty()
                solar_grade(
                    hw_desc, student_code, test_output, error, solar_res_box.markdown
                )

            with st.spinner("⏳ Checking your code with AI-TA (Mistral)..."):
                st.info("💬 Commmments and Grade from Mistral AI-TA:")
                mistral_res_box = st.empty()
                solar_grade(
                    hw_desc,
                    student_code,
                    test_output,
                    error,
                    mistral_res_box.markdown,
                    model=MISTRAL_MODEL,
                )

           

            with st.spinner("⏳ Checking your code with AI-TA (Qwen)..."):
                st.info("💬 Commmments and Grade from Qwen AI-TA:")
                qwen_res_box = st.empty()
                solar_grade(
                    hw_desc,
                    student_code,
                    test_output,
                    error,
                    qwen_res_box.markdown,
                    model=QWEN_MODEL,
                )

            st.success("🎉 AI-TA finished grading your code!")

            if False and st.button("Show AI-TA (GPT)'s comments"):
                st.info("⏳ Checking your code with AI-TA (GPT)...")
                gpt_res_box = st.empty()
                ta_comments = gpt_grade(
                    hw_desc, student_code, test_output, error, gpt_res_box.markdown
                )
                st.success("🎉 AI-TA (GPT) finished grading your code!")
        else:
            st.error("Code execution failed. Please check your code.")
