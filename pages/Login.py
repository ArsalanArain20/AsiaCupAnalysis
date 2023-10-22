import streamlit as st
import time
import Database_Handling as DB

st.set_page_config(layout="wide", page_title="Login")
st.title("Login Now")

# Form for Login
with st.form("Login_Form"):
    Email = st.text_input("Enter your Email")
    Password = st.text_input("Enter your Password", type="password")
    submit_button = st.form_submit_button("Login")

if submit_button:
    # Handle login logic here
    if Email != "" and Password != "":
        response = DB.obj.fetch(Email, Password)
        if response == 1:
            bar = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.1)
                bar.progress(i)
            st.snow()
            st.success("You have successfully logged in")
        else:
            st.error("Invalid email or password")
    else:
        st.error("Please fill in all fields to enable the Login button.")

