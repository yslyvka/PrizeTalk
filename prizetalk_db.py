import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
import os
#import bcrypt

ROLE_CHOICES = (
    'user',
    'moderator',
    'admin',
    'data_curator',
    'staff_admin',
)

mysql_pwd = os.environ.get("MYSQL_PWD")

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=mysql_pwd
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS prizetalk")
cursor.close()
conn.close()

# --- Database connection configuration ---
configuration = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": mysql_pwd,  # Update with your MySQL password
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

AWARD_MAPPING = {
    "booker_prize": "Booker Prize",
    "golden_globes": "Golden Globes",
    "grammy": "Grammy",
    "nobel_laureates": "Nobel Prizes",
    "nobel_prizes": "Nobel Prizes",
    "oscars": "Oscars"
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

    # Award categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS award_categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(255) NOT NULL,
            award_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Tags table (global tagging system)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tag_name VARCHAR(100) UNIQUE NOT NULL
        );
    """)


    # Discussion groups table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discussion_groups (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_by INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    # Community posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            category_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES award_categories(id) ON DELETE CASCADE
        );
    """)

    # Post comments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT NOT NULL,
            user_id INT NOT NULL,
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES community_posts(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    # User roles table (one-to-many from users)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_roles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            role ENUM('user','moderator','admin','data_curator','staff_admin') NOT NULL DEFAULT 'user',
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    # Ensure the enum definition always contains the latest roles
    try:
        enum_values = ",".join(f"'{value}'" for value in ROLE_CHOICES)
        cursor.execute(
            f"""
            ALTER TABLE user_roles
            MODIFY role ENUM({enum_values}) NOT NULL DEFAULT 'user'
            """
        )
    except Exception as enum_error:
        print(f"Warning: could not update user_roles enum: {enum_error}")

    # Group memberships table (users join discussion groups)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_memberships (
            id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT NOT NULL,
            user_id INT NOT NULL,
            role ENUM('member','moderator','admin') NOT NULL DEFAULT 'member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES discussion_groups(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY uniq_group_user (group_id, user_id)
        );
    """)

    # Group posts table (private posts inside groups)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            group_id INT NOT NULL,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES discussion_groups(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    # Group post comments table (threaded)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_post_comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT NOT NULL,
            user_id INT NOT NULL,
            parent_comment_id INT NULL,
            comment_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES group_posts(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (parent_comment_id) REFERENCES group_post_comments(id) ON DELETE SET NULL
        );
    """)

    # Comment reviews table (moderation for public comments)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comment_reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            comment_id INT NOT NULL,
            flagged_by INT NOT NULL,
            reason TEXT,
            status ENUM('pending','approved','removed') NOT NULL DEFAULT 'pending',
            reviewed_by INT NULL,
            reviewed_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (comment_id) REFERENCES post_comments(id) ON DELETE CASCADE,
            FOREIGN KEY (flagged_by) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
        );
    """)

    # Post reports table (moderation for posts)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT NOT NULL,
            reported_by INT NOT NULL,
            reason TEXT,
            status ENUM('pending','reviewed','dismissed') NOT NULL DEFAULT 'pending',
            reviewed_by INT NULL,
            reviewed_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES community_posts(id) ON DELETE CASCADE,
            FOREIGN KEY (reported_by) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
        );
    """)

    # Reactions for public posts/comments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            post_id INT NULL,
            comment_id INT NULL,
            reaction_type ENUM('like','dislike','applause','insightful') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES community_posts(id) ON DELETE CASCADE,
            FOREIGN KEY (comment_id) REFERENCES post_comments(id) ON DELETE CASCADE
        );
    """)

    # Reactions for group posts/comments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reactions_group (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            post_id INT NULL,
            comment_id INT NULL,
            reaction_type ENUM('like','dislike','applause','insightful') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES group_posts(id) ON DELETE CASCADE,
            FOREIGN KEY (comment_id) REFERENCES group_post_comments(id) ON DELETE CASCADE
        );
    """)

    # Bookmarks table (users can bookmark community posts or award references)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            post_id INT NULL,
            award_reference VARCHAR(255) NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES community_posts(id) ON DELETE CASCADE
        );
    """)

    # Notifications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            type VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            is_read BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    # Many-to-many mappings for public posts and tags
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_tags (
            post_id INT,
            tag_id INT,
            PRIMARY KEY (post_id, tag_id),
            FOREIGN KEY (post_id) REFERENCES community_posts(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );
    """)

    # Many-to-many mappings for group posts and tags
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS post_tags_group (
            post_id INT NOT NULL,
            tag_id INT NOT NULL,
            PRIMARY KEY (post_id, tag_id),
            FOREIGN KEY (post_id) REFERENCES group_posts(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );
    """)

# --- CSV Import using pandas ---
def import_csv_with_pandas(table_name, csv_file, cursor):
    print(f"📥 Importing {csv_file} into {table_name}...")
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.ParserError:
        # Try with tab delimiter if comma fails
        try:
            df = pd.read_csv(csv_file, sep='\t')
        except Exception as e:
            print(f"❌ Failed to read {csv_file}: {e}")
            return
    except FileNotFoundError:
        print(f"❌ File not found: {csv_file}")
        return
    except Exception as e:
        print(f"❌ Error reading {csv_file}: {e}")
        return

    # Clean column names: strip spaces, replace spaces with underscores, remove special chars
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('.', '_').str.replace('(', '').str.replace(')', '').str.replace('Only_fiction_novels', 'Only_fiction_novels')

    from urllib.parse import quote_plus
    password = quote_plus(configuration['password'])
    engine = create_engine(
        f"mysql+mysqlconnector://{configuration['user']}:{password}@{configuration['host']}:{configuration['port']}/{configuration['database']}"
    )

    try:
        df.to_sql(table_name, con=engine, if_exists="replace", index=False, chunksize=5000)
        print(f"✅ Imported {len(df)} rows into {table_name}")
    except Exception as e:
        print(f"❌ Failed to import into {table_name}: {e}")
        return

    # Add award_id if applicable
    if table_name in AWARD_MAPPING:
        award_name = AWARD_MAPPING[table_name]
        try:
            # Drop existing FK if any
            cursor.execute(f"""
                SELECT CONSTRAINT_NAME FROM information_schema.TABLE_CONSTRAINTS
                WHERE TABLE_NAME = '{table_name}' AND CONSTRAINT_TYPE = 'FOREIGN KEY'
            """)
            fk_result = cursor.fetchone()
            if fk_result:
                fk_name = fk_result[0]
                cursor.execute(f"ALTER TABLE {table_name} DROP FOREIGN KEY {fk_name}")
            
            # Drop column if exists
            cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'award_id'")
            if cursor.fetchone():
                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN award_id")
            
            # Add column
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN award_id INT")
            
            # Update values
            cursor.execute(f"""
                UPDATE {table_name}
                SET award_id = (SELECT id FROM award_categories WHERE award_name = %s)
            """, (award_name,))
            
            # Add FK
            cursor.execute(f"ALTER TABLE {table_name} ADD FOREIGN KEY (award_id) REFERENCES award_categories(id)")
            
            print(f"✅ Added award_id FK to {table_name}")
        except Exception as e:
            print(f"❌ Failed to add award_id to {table_name}: {e}")

def populate_award_categories(cursor):
    awards = [
        ('Booker Prize', 'Literature'),
        ('Golden Globes', 'Entertainment'),
        ('Grammy', 'Music'),
        ('Nobel Prizes', 'Science/Literature/Peace'),
        ('Oscars', 'Film')
    ]
    for award_name, category in awards:
        cursor.execute("""
            INSERT IGNORE INTO award_categories (award_name, category_name)
            VALUES (%s, %s)
        """, (award_name, category))

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

        # Populate award categories
        populate_award_categories(cursor)

        # Step 2: Setup login system
        # setup_login_system(cursor)

        # Step 3: Import CSVs
        for table_name, csv_file in CSV_FILES.items():
            import_csv_with_pandas(table_name, csv_file, cursor)

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