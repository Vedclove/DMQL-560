import streamlit as st
import psycopg2
import pandas as pd

# Title
st.title("CSE 560 - Bank Database - Team 12 🚀")

# Database connection parameters
db_config = {
    "host": "ep-nameless-snow-a48hdbkf.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_Yx3iRdyceB4h",
    "port": 5432,
    "sslmode": "require"
}

# Function to connect to Neon
@st.cache_resource
def get_connection():
    conn = psycopg2.connect(
        host=db_config["host"],
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        port=db_config["port"],
        sslmode=db_config["sslmode"]
    )
    return conn

# Function to check if query is safe
def is_safe_query(query):
    forbidden = ["drop", "delete", "truncate", "alter"]
    query_lower = query.lower()
    return not any(word in query_lower for word in forbidden)

# SQL input box
query = st.text_area("Enter your SQL query here (SELECT only!):", height=150)

# Run button
if st.button("Run Query"):
    if query.strip() != "":
        if is_safe_query(query):
            try:
                conn = get_connection()
                df = pd.read_sql_query(query, conn)
                st.success("Query executed successfully!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.error("⚠️ Dangerous query detected! Only SELECT queries are allowed.")
    else:
        st.warning("Please enter a SQL query to run.")
