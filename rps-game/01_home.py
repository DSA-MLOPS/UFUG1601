import streamlit as st
from PIL import Image


image = Image.open('qr.jpg')
st.title("Home Page")
st.write("Welcome to the Tic-Tac-Toe Tournament platform!")
st.image(image, caption='QR Code for the Tic-Tac-Toe Tournament')