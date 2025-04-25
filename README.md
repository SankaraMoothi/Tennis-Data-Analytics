Here's the **README** file template you can use for your project:

```markdown
# Tennis Data Analytics with SportRadar API

## Overview
This project leverages the SportRadar API to extract tennis data, store it in a MySQL database, and visualize the data with a Streamlit web application. It provides insights into tennis competitions, rankings, venues, and competitors, offering analytics through various filters.

---

## Project Structure

```plaintext
Tennis-Data-Analytics/
│
├── api_scripts/                # Python scripts for fetching data from SportRadar API
│   ├── fetch_categories_competitions.py     # Fetch categories data competitions data
│   ├── fetch_complexes_venues.py      # Fetch complexes data venues data
│   └── fetch_rankings.py       # Fetch competitor rankings
│
├── db/                   # MySQL schema and queries
│   └── schema.sql              # MySQL schema for tables
│
├── streamlit_app/              # Streamlit app for data visualization
│   └── app.py                  # Main app file
│
├── .env                        # Environment variables for API keys and DB credentials
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## Env

SPORT_RADAR_API_KEY=QWERTYUIOPLKJHGFDSA
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=PASSWORD
DB_NAME=tennis_data

## Prerequisites

Before running the project, you will need the following:

- **MySQL Database**: Ensure you have MySQL installed and configured with the proper credentials.
- **SportRadar API Key**: Obtain an API key from SportRadar to access tennis data.

---

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/SankaraMoothi/Tennis-Data-Analytics.git
    cd Tennis-Data-Analytics
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables**:
   - Create a `.env` file in the root of the project with the following content:
    ```env
    API_KEY=your_sportradar_api_key
    DB_HOST=your_mysql_host
    DB_USER=your_mysql_user
    DB_PASSWORD=your_mysql_password
    DB_NAME=your_database_name
    ```

4. **Set up MySQL Database**:
    - Run the SQL schema:
      ```bash
      mysql -u your_mysql_user -p your_database_name < database/schema.sql
      ```
    - This will create the necessary tables in your database.

---

## Running the Project

### Step 1: Fetch Data from SportRadar API
Run the Python scripts to fetch data from the SportRadar API and populate the database.

```bash
python api_scripts/fetch_categories_competitions.py
python api_scripts/fetch_complexes_venues.py
python api_scripts/fetch_rankings.py
```

### Step 2: Run the Streamlit App
Start the Streamlit app to visualize the data.

```bash
streamlit run streamlit_app/app.py
```

---

## Features

- **Homepage Dashboard:**
  - Summary statistics such as:
    - Total number of competitors.
    - Number of countries represented.
    - Highest points scored by a competitor.

- **Search and Filter Competitors:**
  - Allows users to search for a competitor by name.
  - Filters competitors by rank range, country, or points threshold.

- **Competitor Details Viewer:**
  - Displays detailed information about a selected competitor, including:
    - Rank, movement, competitions played, and country.

- **Country-Wise Analysis:**
  - Lists countries with the total number of competitors and their average points.

- **Leaderboards:**
  - Displays top-ranked competitors.
  - Competitors with the highest points.
  - Stable rank competitors (no movement).

- **Venues:**
  - Lists venues with associated complex names.
  - Allows filtering of venues by country.


---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

---

This README will provide an easy-to-follow guide for setting up and running the project. Let me know if you'd like to add any other details or modifications!