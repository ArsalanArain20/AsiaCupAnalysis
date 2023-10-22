# Importing Liberary
import streamlit as st
import json
import Database_Handling as DB

# Page Layout
st.set_page_config(layout="wide",page_title="Register")

# title
st.title("Register Now")
# Registration form
with st.form("Register_Form"):
    # Add form elements
    Name = st.text_input("Enter Your Name")
    Email = st.text_input("Enter your Email")
    Password = st.text_input("Enter your Password", type="password")
    Re_Password = st.text_input("Enter your Confirm Password", type="password")
    Favt_Player = st.text_input("Enter your Favourite Cricketer")

    # Create a submit button
    submit_button = st.form_submit_button("Register")

# Process the form submission
if submit_button:
    if Email != "" and Password != "" and Re_Password != "" and Name != "" and Favt_Player != "":
        if Password == Re_Password:
            U = DB.obj.insert(Name,Email,Password,Re_Password,Favt_Player)
            if U == 1:
                st.balloons()
                st.success("Congragulations Successfully Registered")
            else:
                st.error("Someone Went Wrong Try Again.")
        else:
            st.error("Password & Retype Password not Matched")
    else:
        st.error("Please fill in all fields to enable the Register button.")


