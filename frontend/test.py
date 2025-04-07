import streamlit as st

# Function to dynamically style the selected sidebar item
def get_sidebar_style(selected_item):
    if selected_item == "Home":
        return "color: white; background-color: #FF6347;"
    elif selected_item == "About":
        return "color: white; background-color: #32CD32;"
    elif selected_item == "Contact":
        return "color: white; background-color: #1E90FF;"
    return "color: white;"

# Sidebar content with selectbox (better control over hover effects using interactive features)
st.sidebar.title("Custom Sidebar")
menu = st.sidebar.radio("Navigation", ["Home", "About", "Contact"])

# Apply dynamic styling to the selected sidebar item
st.sidebar.markdown(f"""
    <style>
        .stRadio > label {{
            {get_sidebar_style(menu)}
        }}
    </style>
""", unsafe_allow_html=True)

# Main content
if menu == "Home":
    st.title("Welcome to Home!")
elif menu == "About":
    st.title("About Us")
else:
    st.title("Contact Us")

st.write("This is a Streamlit app with custom interactivity and style.")
