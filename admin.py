import streamlit as st
import sqlite3
import pandas as pd

# Function to fetch data from the database
def fetch_data():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()
    return data

# Streamlit admin dashboard
st.title("Admin Dashboard")

# Fetch data from the database
st.header("Registered Students")
data = fetch_data()

if data:
    # Convert the data to a Pandas DataFrame for better display
    df = pd.DataFrame(data, columns=["ID", "First Name", "Last Name", "Age", "Gender", "Weight", "Address"])
    st.dataframe(df)

    # Option to download the data as a CSV file
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="students_data.csv",
        mime="text/csv"
    )

else:
    st.warning("No data available yet.")

# Add additional filters or analytics if needed
st.sidebar.header("Filters")
filter_gender = st.sidebar.selectbox("Filter by Gender", ["All", "Male", "Female", "Other"])

if filter_gender != "All":
    df = df[df["Gender"] == filter_gender]
    st.dataframe(df)

    if not df.empty:
        st.success(f"Filtered {len(df)} record(s) for gender: {filter_gender}")
    else:
        st.warning(f"No records found for gender: {filter_gender}")
