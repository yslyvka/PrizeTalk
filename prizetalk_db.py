import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
import bcrypt

# --- Database connection configuration ---
configuration = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Ternopil@2007",  # Update with your MySQL password
    "database": "prizetalk",
    "allow_local_infile": True
}

# CSV files in Public_Data folder
CSV_FILES = {
    "booker_prize": "Public_Data/Booker Prize Dataset Final.csv",
    "golden_globes": "Public_Data/Golden_Globes_Awards_Dataset.csv",
    "grammy": "Public_Data/Grammy Award Nominees and Winners 1958-2024.csv",
    "nobel_laureates": "Public_Data/nobel_laureates.csv",
    "nobel_prizes": "Public_Data/nobel_prizes.csv",
    "oscars": "Public_Data/oscars.csv"
}

# --- Schema creation ---
def create_tables(cursor):
    # Users table for login system
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

# --- CSV Import using pandas ---
def import_csv_with_pandas(table_name, csv_file):
    print(f"📥 Importing {csv_file} into {table_name}...")
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.ParserError:
        # Try with tab delimiter if comma fails
        df = pd.read_csv(csv_file, sep='\t')

    # Clean column names: strip spaces, replace spaces with underscores, remove special chars
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('.', '_').str.replace('(', '').str.replace(')', '').str.replace('Only_fiction_novels', 'Only_fiction_novels')

    from urllib.parse import quote_plus
    password = quote_plus(configuration['password'])
    engine = create_engine(
        f"mysql+mysqlconnector://{configuration['user']}:{password}@{configuration['host']}:{configuration['port']}/{configuration['database']}"
    )

    df.to_sql(table_name, con=engine, if_exists="replace", index=False, chunksize=5000)
    print(f"✅ Imported {len(df)} rows into {table_name}")

# --- Simple login system setup ---
def setup_login_system(cursor):
    # Insert a sample user (with properly hashed password)
    hashed_password = bcrypt.hashpw("adminpassword".encode(), bcrypt.gensalt()).decode()
    cursor.execute("""
        REPLACE INTO users (username, password_hash, email)
        VALUES (%s, %s, %s)
    """, ("admin", hashed_password, "admin@example.com"))

# --- Query runner ---
def run_query(cursor, name, sql, params=None, limit_print=None):
    print(f"\n--- {name.upper()} ---")
    try:
        cursor.execute(sql, params or ())
    except Exception as e:
        print(f"Query execution error for {name}: {e}")
        print("SQL:", sql)
        print("PARAMS:", params)
        return
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    rows = cursor.fetchall() if cursor.description else []
    if limit_print:
        rows_to_show = rows[:limit_print]
        print(f"Showing {len(rows_to_show)} of {len(rows)} rows")
    else:
        rows_to_show = rows
        print(f"Total rows: {len(rows)}")
    for row in rows_to_show:
        print(dict(zip(columns, row)))

# --- Main ---
def main():
    try:
        conn = mysql.connector.connect(**configuration)
        cursor = conn.cursor()

        # Step 1: Create tables
        create_tables(cursor)

        # Step 2: Setup login system
        setup_login_system(cursor)

        # Step 3: Import CSVs
        for table_name, csv_file in CSV_FILES.items():
            import_csv_with_pandas(table_name, csv_file)

        conn.commit()

    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()