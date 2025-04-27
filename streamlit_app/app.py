


import streamlit as st
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os
import plotly.express as px

# Load environment variables
load_dotenv()

# Database connection
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Helper to fetch data
def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.sidebar.title("🎾 Tennis Analytics")
page = st.sidebar.radio("Navigate", [
    "🏠 Dashboard", "🔍 Competitor Search", "👤 Competitor Details",
    "🌍 Country Analysis", "📈 Leaderboards", "📅 Competitions", "🏟️ Venues"
])

# Dashboard
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", fetch_data("SELECT COUNT(*) as count FROM competitors")['count'][0])
    col2.metric("Countries Represented", fetch_data("SELECT COUNT(DISTINCT country) as count FROM competitors")['count'][0])
    col3.metric("Highest Points", fetch_data("SELECT MAX(points) as max FROM competitor_rankings")['max'][0])

# Competitor Search
elif page == "🔍 Competitor Search":
    st.title("🔍 Search Competitors")
    name = st.text_input("Search by Name")
    country = st.text_input("Filter by Country")
    rank_range = st.slider("Rank Range", 1, 1000, (1, 100))

    query = f"""
        SELECT c.name, c.country, r.rank, r.points
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        WHERE r.rank BETWEEN {rank_range[0]} AND {rank_range[1]}
    """
    if name:
        query += f" AND c.name LIKE '%{name}%'"
    if country:
        query += f" AND c.country LIKE '%{country}%'"

    st.dataframe(fetch_data(query))

# Competitor Details
elif page == "👤 Competitor Details":
    st.title("👤 Competitor Details")
    competitors = fetch_data("SELECT name FROM competitors ORDER BY name")['name'].tolist()
    selected = st.selectbox("Select competitor", competitors)

    detail_query = f"""
        SELECT c.name, c.country, r.rank, r.movement, r.points, r.competitions_played
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        WHERE c.name = '{selected}'
    """
    st.dataframe(fetch_data(detail_query))

# Country Analysis
elif page == "🌍 Country Analysis":
    st.title("🌍 Country-Wise Analysis")
    query = """
        SELECT country, COUNT(*) as total_competitors, AVG(points) as avg_points
        FROM competitors c
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        GROUP BY country
    """
    df = fetch_data(query)
    st.dataframe(df)
    st.plotly_chart(px.bar(df, x='country', y='total_competitors', title="Competitors per Country"))

# Leaderboards
elif page == "📈 Leaderboards":
    st.title("🏅 Leaderboards")
    choice = st.radio("Leaderboard Type", ["Top Rank", "Highest Points", "Stable Rank"])

    try:
        if choice == "Top Rank":
            query = """
                SELECT c.name, r.rank, r.points
                FROM competitors c
                JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
                ORDER BY r.rank ASC
                LIMIT 5
            """
        elif choice == "Highest Points":
            query = """
                SELECT c.name, r.rank, r.points
                FROM competitors c
                JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
                ORDER BY r.points DESC
                LIMIT 5
            """
        elif choice == "Stable Rank":
            query = """
                SELECT c.name, r.rank, r.movement
                FROM competitors c
                JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
                WHERE r.movement = 0
            """

        # Fetch data using the modified query
        df = fetch_data(query)

        # If data is empty, show a message
        if df.empty:
            st.write("No data found for the selected leaderboard type.")
        else:
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error fetching leaderboard data: {e}")

# Competitions
elif page == "📅 Competitions":
    st.title("📅 Competitions")

    # Queries as per requirement
    queries = {
        "All competitions with category": "SELECT competition_name, category_name FROM competitions JOIN categories ON competitions.category_id = categories.category_id",
        "Count competitions per category": "SELECT category_name, COUNT(*) as total FROM competitions JOIN categories ON competitions.category_id = categories.category_id GROUP BY category_name",
        "Doubles Competitions": "SELECT * FROM competitions WHERE type = 'doubles'",
        "Competitions in 'ITF Men'": "SELECT * FROM competitions JOIN categories ON competitions.category_id = categories.category_id WHERE category_name = 'ITF Men'",
        "Parent & Sub Competitions": "SELECT parent.competition_name AS parent, child.competition_name AS child FROM competitions parent JOIN competitions child ON parent.competition_id = child.parent_id",
        "Type Distribution by Category": "SELECT category_name, type, COUNT(*) as total FROM competitions JOIN categories ON competitions.category_id = categories.category_id GROUP BY category_name, type",
        "Top-level Competitions": "SELECT competition_name FROM competitions WHERE parent_id IS NULL"
    }

    selected_query = st.selectbox("Choose Query", list(queries.keys()))
    st.dataframe(fetch_data(queries[selected_query]))

# Venues
elif page == "🏟️ Venues":
    st.title("🏟️ Venues")

    queries = {
        "Venues with Complex Name": "SELECT v.name AS venue_name, v.city_name, v.country_name, v.timezone, c.name AS complex_name FROM venues v LEFT JOIN complexes c ON v.complex_id = c.complex_id",
        "Venue Count per Complex": "SELECT c.name AS complex_name, COUNT(*) as total_venues FROM venues v JOIN complexes c ON v.complex_id = c.complex_id GROUP BY c.name",
        "Venues in Chile": "SELECT * FROM venues WHERE country_name = 'Chile'",
        "Venues and Timezones": "SELECT name AS venue_name, timezone FROM venues",
        "Complexes with Multiple Venues": "SELECT complex_id, COUNT(*) FROM venues GROUP BY complex_id HAVING COUNT(*) > 1",
        "Venues by Country": "SELECT country_name, COUNT(*) as total FROM venues GROUP BY country_name",
        "Venues for 'Nacional' Complex": "SELECT v.name FROM venues v JOIN complexes c ON v.complex_id = c.complex_id WHERE c.name = 'Nacional'"
    }

    selected_query = st.selectbox("Choose Query", list(queries.keys()))
    st.dataframe(fetch_data(queries[selected_query]))
