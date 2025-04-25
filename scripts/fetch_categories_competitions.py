import os
import requests
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_URL = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"
API_KEY = os.getenv("SPORT_RADAR_API_KEY")

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Fetch competition data from API
def fetch_competitions():
    response = requests.get(f"{API_URL}?api_key={API_KEY}")
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()

# Insert categories and competitions into DB
def insert_competitions_data(db_conn, competitions):
    cursor = db_conn.cursor()
    try:
        for item in competitions:
            # Extract competition and category info
            competition_id = item['id']
            competition_name = item['name']
            parent_id = item.get('parent_id')
            comp_type = item['type']
            gender = item['gender']
            category = item['category']
            category_id, category_name = category['id'], category['name']

            # Insert/update category (no delete)
            cursor.execute(
                """
                INSERT INTO Categories (category_id, category_name)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE category_name = VALUES(category_name)
                """,
                (category_id, category_name)
            )

            # Replace competition (safe since it's not referenced yet)
            cursor.execute(
                """
                REPLACE INTO Competitions (
                    competition_id, competition_name, parent_id,
                    type, gender, category_id
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (competition_id, competition_name, parent_id, comp_type, gender, category_id)
            )

        db_conn.commit()
        print("✅ Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        db_conn.rollback()
    finally:
        cursor.close()

# Main runner
def main():
    try:
        data = fetch_competitions()
        competitions = data.get('competitions', [])
        if not competitions:
            print("⚠️ No competition data found.")
            return

        db_conn = get_db_connection()
        insert_competitions_data(db_conn, competitions)
        db_conn.close()

    except requests.RequestException as e:
        print(f"❌ API request failed: {e}")
    except mysql.connector.Error as e:
        print(f"❌ MySQL connection error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
