import streamlit as st
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                gender TEXT,
                weight REAL,
                address TEXT)''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(first_name, last_name, age, gender, weight, address):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (first_name, last_name, age, gender, weight, address) VALUES (?, ?, ?, ?, ?, ?)",
              (first_name, last_name, age, gender, weight, address))
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Streamlit app
st.title("Student Registration Form")

# Create the registration form
with st.form("registration_form"):
    st.header("Enter Your Details")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    address = st.text_area("Address")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not first_name or not last_name or not address:
            st.error("Please fill in all required fields.")
        else:
            insert_data(first_name, last_name, age, gender, weight, address)
            st.success("Registration successful!")

# Deployment instructions
st.info("Once deployed, share the app link with students to collect their details.")
