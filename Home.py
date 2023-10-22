# Importing Liberary
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide",page_title="Cricket Asiacup")

# Page Overview
st.title("Asian Cricket Council (ACC)")
st.image("cricket-images/cover.jpg")
col1,col2 = st.columns(2)
with col1:
    st.image("cricket-images/header2.jpg")
with col2:
    st.image("cricket-images/side.jpg")

st.title("ALL Time Participate Teams")
# partispeateing team pics round 1
team1,team2,team3,team4 = st.columns(4)
with team1:
    st.image("logo-images/BCCI_logo.png")
with team2:
    st.image("logo-images/pcb-logo.png")
with team3:
    st.image("logo-images/sirlanka-logo.png")
with team4:
    st.image("logo-images/bangaladesh-logo.png")

# partispeateing team pics round 1
team5,team6,team7,team8 = st.columns(4)
with team5:
    st.image("logo-images/afganistan-logo.png")
with team6:
    st.image("logo-images/uae-logo.png")
with team7:
    st.image("logo-images/nepal-logo.png")
with team8:
    st.image("logo-images/hongcong-logo.png")








