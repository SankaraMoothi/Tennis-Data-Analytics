import os
import requests
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("SPORT_RADAR_API_KEY")
VENUES_API_URL = f"https://api.sportradar.com/tennis/trial/v3/en/complexes.json?api_key={API_KEY}"

# Get DB connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Fetch venues data from API
def fetch_venues():
    response = requests.get(VENUES_API_URL)
    response.raise_for_status()  # Raise error on failure
    return response.json()

# Insert venues & complexes into the DB
def insert_venues_data(db_conn, complexes):
    cursor = db_conn.cursor()
    try:
        for complex_item in complexes:
            # Complex info
            complex_id = complex_item['id']
            complex_name = complex_item['name']
            cursor.execute(
                "REPLACE INTO Complexes (complex_id, name) VALUES (%s, %s)",
                (complex_id, complex_name)
            )

            # Insert venues for each complex
            for venue_item in complex_item.get('venues', []):
                venue_id = venue_item['id']
                venue_name = venue_item['name']
                city_name = venue_item.get('city_name')
                country_name = venue_item.get('country_name')
                country_code = venue_item.get('country_code')
                timezone = venue_item.get('timezone')

                cursor.execute(
                    """
                    REPLACE INTO Venues (
                        venue_id, name, city_name,
                        country_name, country_code,
                        timezone, complex_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
                )

        db_conn.commit()
        print("✅ Venues and complexes inserted successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        db_conn.rollback()
    finally:
        cursor.close()

# Main entry point
def main():
    try:
        data = fetch_venues()
        # Extract complexes data from the response
        complexes = data.get('complexes', [])
        if not complexes:
            print("⚠️ No complexes found in response.")
            return

        db_conn = get_db_connection()
        insert_venues_data(db_conn, complexes)
        db_conn.close()

    except requests.RequestException as e:
        print(f"❌ API request failed: {e}")
    except mysql.connector.Error as e:
        print(f"❌ Database connection error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
