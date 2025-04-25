import os
import requests
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("SPORT_RADAR_API_KEY")
RANKINGS_API_URL = f"https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json?api_key={API_KEY}"

# Get DB connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Fetch rankings data from API
def fetch_rankings():
    try:
        response = requests.get(RANKINGS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ API request failed: {e}")
        return None

# Insert data into database
def insert_data(db_conn, data):
    cursor = db_conn.cursor()
    try:
        rankings = data.get('rankings', [])
        for ranking in rankings:
            type_name = ranking.get('name')
            year = ranking.get('year')
            week = ranking.get('week')
            gender = ranking.get('gender')
            type_id = ranking.get('type_id')

            for r in ranking.get('competitor_rankings', []):
                competitor = r['competitor']
                comp_id = competitor['id']
                name = competitor['name']
                country = competitor.get('country', '')
                country_code = competitor.get('country_code', '')
                abbreviation = competitor.get('abbreviation', '')

                # Insert or update Competitor
                cursor.execute("""
                    REPLACE INTO Competitors (competitor_id, name, country, country_code, abbreviation)
                    VALUES (%s, %s, %s, %s, %s)
                """, (comp_id, name, country, country_code, abbreviation))

                # Insert Competitor Ranking
                cursor.execute("""
                    INSERT INTO Competitor_Rankings (
                        `rank`, movement, points, competitions_played,
                        competitor_id
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    r['rank'], r['movement'], r['points'], r['competitions_played'],
                    comp_id
                ))

        db_conn.commit()
        print("✅ Competitor rankings inserted successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        db_conn.rollback()
    finally:
        cursor.close()

# Main entry point
def main():
    data = fetch_rankings()
    if not data:
        print("⚠️ No data returned.")
        return

    try:
        db_conn = get_db_connection()
        insert_data(db_conn, data)
        db_conn.close()
    except mysql.connector.Error as e:
        print(f"❌ Database connection error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
