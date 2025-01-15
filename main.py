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
    c.execute('''CREATE TABLE IF NOT EXISTS admin (
                username TEXT PRIMARY KEY,
                password TEXT)''')
    conn.commit()

    # Add default admin credentials if not exists
    c.execute("INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)", ("admin", "password"))
    conn.commit()
    conn.close()

# Function to insert data into the students database
def insert_data(first_name, last_name, age, gender, weight, address):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (first_name, last_name, age, gender, weight, address) VALUES (?, ?, ?, ?, ?, ?)",
              (first_name, last_name, age, gender, weight, address))
    conn.commit()
    conn.close()

# Function to verify admin credentials
def verify_admin(username, password):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

# Function to fetch all student data
def fetch_all_students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return data

# Initialize the database
init_db()

# Streamlit app
st.title("Student Registration and Admin Dashboard")

menu = st.sidebar.selectbox("Menu", ["Registration", "Admin Login"])

if menu == "Registration":
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

elif menu == "Admin Login":
    st.header("Admin Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if verify_admin(username, password):
            st.success("Login successful!")

            # Display the admin dashboard
            st.header("Admin Dashboard")
            st.subheader("Registered Students")

            student_data = fetch_all_students()
            if student_data:
                for student in student_data:
                    st.text(f"ID: {student[0]} | Name: {student[1]} {student[2]} | Age: {student[3]} | Gender: {student[4]} | Weight: {student[5]} | Address: {student[6]}")
            else:
                st.info("No students registered yet.")
        else:
            st.error("Invalid username or password.")
