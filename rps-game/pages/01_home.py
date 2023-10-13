import streamlit as st
from PIL import Image

image = Image.open('qr.jpg')
st.title("Home Page")
st.write("Welcome to the Rock-Paper-Scissors Tournament platform!")
st.image(image, caption='QR Code for the Rock-Paper-Scissors Tournament')