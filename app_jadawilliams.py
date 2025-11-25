# ============================================
# Restaurant Dashboard - Streamlit Application Template
# ITOM6265 - Database Homework
#
# INSTRUCTIONS:
# 1. Update database credentials in Block 3
# 2. Fill in all TODO sections
# 3. Test each tab individually
# 4. Read the hints and documentation links
# ============================================

# Block 1: Import required libraries (KEEP THIS AS-IS)
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import folium
from streamlit_folium import st_folium

# Block 2: Page configuration (KEEP THIS AS-IS)
st.set_page_config(
    page_title="ITOM6265-HW1",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Block 3: Database connection (UPDATE CREDENTIALS ONLY)
# ===== UPDATE THESE VALUES WITH YOUR DATABASE INFORMATION =====
try:
    connection = mysql.connector.connect(
        host='db-mysql-itom-do-user-28250611-0.j.db.ondigitalocean.com',  # TODO: Update with your host
        port=25060,  # TODO: Update with your port (usually 3306 for local, 25060 for DigitalOcean)
        user='restaurant_readonly',  # TODO: Update with your username
        password='SecurePassword123!',  # TODO: Update with your password
        database='restaurant'  # TODO: Update with your database name
    )
    db_connected = True
    st.success("✅ Database connected successfully!")
except Error as e:
    st.error(f"❌ Error connecting to MySQL Database: {e}")
    st.info("Please check your database credentials in the code (Block 3)")
    db_connected = False
    connection = None

# Block 4: Sidebar navigation (KEEP THIS AS-IS)
st.sidebar.title("🍽️ ITOM6265-HW1")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["HW Summary", "Q1-DB Query", "Q2-Maps"],
    help="Select a page to navigate"
)
st.sidebar.markdown("---")
st.sidebar.info("Restaurant Database Dashboard")

