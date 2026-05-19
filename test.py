import streamlit as st

# Check if the user is authenticated
if not st.user.is_logged_in:
    st.write("You are not logged in.")
    if st.button("Log in with Google"):
        st.login("google")
    st.stop()  # Halt further execution until logged in

# App content for authenticated users
st.write(f"Welcome to the dashboard, {st.user.name}!")
st.write(f"Your email is: {st.user.email}")

if st.button("Log out"):
    st.logout()
  
