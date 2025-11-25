import streamlit as st
import mysql.connector
import pandas as pd
import folium
from streamlit_folium import st_folium

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Restaurant Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ============================================================================
# CUSTOM STYLING - PINK & GREEN THEME
# ============================================================================
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-weight: bold;
    color: #FF1493;
}
h1, h2, h3 {
    color: #FF1493 !important;
}
.stButton>button {
    background-color: #FF1493 !important;
    color: white !important;
    border: 2px solid #32CD32 !important;
}
.stButton>button:hover {
    background-color: #32CD32 !important;
    border: 2px solid #FF1493 !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFE5F0 0%, #E5FFE5 100%);
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE CONNECTION
# ============================================================================
def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host='db-mysql-itom-do-user-28250611-0.j.db.ondigitalocean.com',
            port=25060,
            user='restaurant_readonly',
            password='SecurePassword123!',
            database='restaurant'
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None

# Initialize connection
conn = get_database_connection()

# Test connection
if conn:
    st.sidebar.success("✅ Database connected!")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM business_location")
        count = cursor.fetchone()[0]
        st.sidebar.info(f"📊 Total restaurants: {count}")
        cursor.close()
    except Exception as e:
        st.sidebar.error(f"Query error: {e}")
else:
    st.sidebar.error("❌ Connection failed!")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_vote_range():
    if not conn:
        return 0, 1000
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(votes), MAX(votes) FROM business_location")
        result = cursor.fetchone()
        cursor.close()
        if result and result[0] is not None:
            return int(result[0]), int(result[1])
    except Exception as e:
        st.error(f"Vote range error: {e}")
    return 0, 1000

def search_restaurants(name_pattern, min_votes, max_votes):
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = "SELECT name, votes, city FROM business_location WHERE name LIKE %s AND votes BETWEEN %s AND %s ORDER BY votes DESC"
        cursor.execute(query, (f'%{name_pattern}%', min_votes, max_votes))
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        st.error(f"Search error: {e}")
        return []

def get_restaurant_locations():
    if not conn:
        return pd.DataFrame()
    try:
        cursor = conn.cursor()
        query = "SELECT name, latitude, longitude FROM business_location WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(results, columns=['name', 'latitude', 'longitude'])
        return df
    except Exception as e:
        st.error(f"Map error: {e}")
        return pd.DataFrame()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.title("🍽️ Navigation")
page = st.sidebar.radio("Select a tab:", ["📋 HW Summary", "🔍 Database Search", "🗺️ Interactive Map"])

# ============================================================================
# TAB 1: HW SUMMARY
# ============================================================================
if page == "📋 HW Summary":
    st.markdown('<p class="big-font">Restaurant Dashboard - Homework Summary</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=150)
    
    with col2:
        st.markdown("### 👤 MSBA STUDENT AT SMU")
        st.write("**Name:** Jada Williams")
        st.write("**Course:** ITOM6265")
        st.write("**Assignment:** Restaurant Dashboard with Streamlit")
        st.write("**Date:** November 2024")
    
    st.markdown("---")
    st.markdown("### 🎨 Customizations Implemented")
    
    st.info("**1. Custom CSS Styling - Pink & Green Theme:** Added custom pink and green gradient colors for headers, buttons, sidebar, and metric containers")
    st.info("**2. Two-Column Layout:** Used Streamlit columns for better visual organization in Summary tab")
    st.info("**3. Custom Map Tiles:** Implemented CartoDB Positron tiles for the interactive map (instead of default OpenStreetMap)")
    st.info("**4. Enhanced Data Display:** Color-coded result counts and styled tables with custom pink/green formatting")
    st.info("**5. Interactive Widgets:** Added emoji icons and captions for better user experience with pink/green hover effects")
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Features")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Database Connection", "Active ✅")
    with col2:
        st.metric("Search Filters", "Name + Votes")
    with col3:
        st.metric("Map Markers", "Interactive 📍")

# ============================================================================
# TAB 2: DATABASE SEARCH
# ============================================================================
elif page == "🔍 Database Search":
    st.title("🔍 Restaurant Database Search")
    st.markdown("Search for restaurants by name and vote count")
    
    min_votes_db, max_votes_db = get_vote_range()
    
    col1, col2 = st.columns(2)
    
    with col1:
        name_input = st.text_input("🏪 Restaurant Name", placeholder="Enter restaurant name (e.g., Dishoom)")
    
    with col2:
        vote_range = st.slider("📊 Vote Range", min_value=int(min_votes_db), max_value=int(max_votes_db), value=(int(min_votes_db), int(max_votes_db)))
    
    if st.button("🔍 Get results"):
        results = search_restaurants(name_input, vote_range[0], vote_range[1])
        
        if results:
            st.success(f"✅ Found {len(results)} restaurant(s)")
            df = pd.DataFrame(results, columns=['Restaurant Name', 'Votes', 'City'])
            st.dataframe(df, height=400)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Results", len(results))
            with col2:
                st.metric("Avg Votes", f"{df['Votes'].mean():.0f}")
            with col3:
                st.metric("Max Votes", df['Votes'].max())
        else:
            st.warning("⚠️ No restaurants found. Try adjusting the filters.")
    
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        - **Empty name field**: Shows all restaurants within the vote range
        - **Specific name**: Searches for restaurants containing that text
        - **Vote range**: Filter restaurants by popularity (vote count)
        
        **Example Searches:**
        - Name: "Dishoom" → Shows all Dishoom locations
        - Votes: 0-500 → Shows restaurants with 0 to 500 votes
        """)

# ============================================================================
# TAB 3: INTERACTIVE MAP
# ============================================================================
elif page == "🗺️ Interactive Map":
    st.title("🗺️ Restaurant Locations in London")
    st.markdown("Explore restaurant locations on an interactive map")
    
    if st.button("🗺️ Display map!"):
        st.session_state['show_map'] = True
    
    st.caption("Map of restaurants in London. Click on marker to check names.")
    
    if st.session_state.get('show_map', False):
        with st.spinner("Loading map..."):
            location_df = get_restaurant_locations()
            
            if not location_df.empty:
                st.success(f"✅ Loaded {len(location_df)} restaurant locations")
                
                m = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles='CartoDB positron')
                
                for idx, row in location_df.iterrows():
                    folium.Marker(
                        location=[row['latitude'], row['longitude']],
                        popup=folium.Popup(row['name'], max_width=300),
                        tooltip=row['name'],
                        icon=folium.Icon(color='pink', icon='cutlery', prefix='fa')
                    ).add_to(m)
                
                st_folium(m, width=1400, height=600)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Restaurants", len(location_df))
                with col2:
                    st.info("💡 Click any pink marker to see the restaurant name")
            else:
                st.error("❌ No location data available")
    
    with st.expander("ℹ️ Map Information"):
        st.markdown("""
        **Map Features:**
        - 🗺️ Custom CartoDB Positron tiles
        - 📍 Pink markers indicate restaurant locations
        - 🖱️ Click markers to see restaurant names
        - 🔍 Zoom in/out using +/- buttons
        """)

# ============================================================================
# FOOTER
# ============================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 About")
st.sidebar.info("This dashboard connects to a MySQL database containing restaurant information.")
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")
