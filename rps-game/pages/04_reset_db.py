import streamlit as st
from db_util import db_execute_query

PASS_CODE = "1234"

st.title("Reset Database")
st.write("Please enter the passcode to reset the database.")

passcode = st.text_input("Passcode:", type="password")

if st.button("Delete All Records"):
    if passcode == PASS_CODE:
        db_execute_query("DELETE FROM students")
        st.success("Database reset successfully!")
    else:
        st.error("Incorrect passcode, please try again!")