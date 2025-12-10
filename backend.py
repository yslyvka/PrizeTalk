from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import platform
import os
from datetime import datetime, date
from decimal import Decimal

AWARD_TABLES = {
    "booker_prize": "Booker Prize",
    "golden_globes": "Golden Globes",
    "grammy": "Grammy Awards",
    "nobel_laureates": "Nobel Laureates",
    "nobel_prizes": "Nobel Prizes",
    "oscars": "Oscars",
}

ALLOWED_ROLES = {'user', 'moderator', 'admin', 'data_curator', 'staff_admin'}

app = Flask(__name__)
CORS(app)  # Allow CORS for Vue dev server

# Determine host based on platform
if platform.system() == 'Windows':
    host = '127.0.0.1'
elif platform.system() == 'Darwin':  # macOS
    host = '127.0.0.1'
else:  # Linux
    if os.path.exists('/mnt/c'):  # WSL
        host = '172.30.128.1'  # Windows host IP from WSL
    else:  # Native Linux (Ubuntu)
        host = '127.0.0.1'

# Database connection
config = {
    "host": host,
    "port": 3306,
    "user": "root",
    "password": "domdh361",  # Update with your MySQL password
    "database": "prizetalk",
}


def get_db(dictionary=False):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=dictionary)
    return connection, cursor

@app.route("/api/awards/tables/", methods=["GET"])
def list_award_tables():
    conn, cursor = get_db(dictionary=True)
    try:
        placeholders = ", ".join(["%s"] * len(AWARD_TABLES))
        cursor.execute(
            f"""
            SELECT TABLE_NAME AS table_name, TABLE_ROWS AS table_rows
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name IN ({placeholders})
            """,
            [config["database"], *AWARD_TABLES.keys()],
        )
        table_info = {
            row["table_name"]: row.get("table_rows", 0) for row in cursor.fetchall()
        }
        response = [
            {
                "table": table_name,
                "display_name": AWARD_TABLES[table_name],
                "row_count": int(table_info.get(table_name) or 0),
            }
            for table_name in AWARD_TABLES.keys()
        ]
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Failed to load award tables: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/awards/tables/<table_name>/", methods=["GET"])
def get_award_table_data(table_name):
    if table_name not in AWARD_TABLES:
        return jsonify({"error": "Unknown award table"}), 404

    try:
        limit = int(request.args.get("limit", 50))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit and offset must be integers"}), 400

    # Safety caps
    limit = max(1, min(limit, 200))
    offset = max(0, offset)

    conn, cursor = get_db(dictionary=True)
    try:
        query = f"SELECT * FROM {table_name} LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        raw_rows = cursor.fetchall()
        columns = list(cursor.column_names) if hasattr(cursor, "column_names") else (list(raw_rows[0].keys()) if raw_rows else [])

        def _serialize_value(value):
            if isinstance(value, Decimal):
                return float(value)
            if isinstance(value, (datetime, date)):
                return value.isoformat()
            return value

        rows = []
        for row in raw_rows:
            shaped = {}
            for col in row.keys():
                shaped[col] = _serialize_value(row.get(col))
            rows.append(shaped)

        return jsonify(
            {
                "table": table_name,
                "display_name": AWARD_TABLES[table_name],
                "columns": columns,
                "rows": rows,
                "limit": limit,
                "offset": offset,
            }
        )
    except Exception as e:
        return jsonify({"error": f"Failed to load table data: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/login/', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, password_hash, username FROM users WHERE email = %s",
            (email,),
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        stored_hash = user['password_hash']
        if isinstance(stored_hash, bytes):
            hash_bytes = stored_hash
        else:
            hash_bytes = stored_hash.encode('utf-8')

        if not bcrypt.checkpw(password.encode('utf-8'), hash_bytes):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

        cursor.execute(
            """
            SELECT role
            FROM user_roles
            WHERE user_id = %s
            ORDER BY assigned_at DESC
            LIMIT 1
            """,
            (user['id'],),
        )
        role_row = cursor.fetchone()
        role = role_row['role'] if role_row else 'user'

        name_parts = (user['username'] or '').split(' ', 1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        response = {
            'kind': 'staff',
            'account': {
                'id': user['id'],
                'username': user['username'],
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'role': role
            },
            'message': 'Login successful',
        }

        return jsonify(response)
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': f'Login failed: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/signup/', methods=['POST'])
def signup():
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')
    
    if not all([first_name, last_name, email, password]):
        return jsonify({'success': False, 'message': 'All fields required'}), 400

    if role not in ALLOWED_ROLES:
        role = 'user'
    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    username = f"{first_name} {last_name}"

    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Email already exists'}), 409

        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
            (username, hashed, email),
        )
        user_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO user_roles (user_id, role) VALUES (%s, %s)",
            (user_id, role),
        )
        conn.commit()

        return jsonify(
            {
                'success': True,
                'message': f"{role.replace('_', ' ').title()} account created successfully.",
                'user': {
                    'id': user_id,
                    'email': email,
                    'firstName': first_name,
                    'lastName': last_name,
                    'role': role,
                },
            }
        )
    except mysql.connector.IntegrityError:
        conn.rollback()
        return jsonify({'success': False, 'message': 'Email already exists'}), 409
    except Exception as e:
        conn.rollback()
        print("SIGNUP RECEIVED:", data)
        print("ROLE BEFORE CHECK:", role)
        print("ALLOWED:", ALLOWED_ROLES)

        print("SIGNUP ERROR:", repr(e))
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/profiles/<int:user_id>/follow/", methods=["POST"])
def follow_user(user_id):
    data = request.json
    current_user_id = data.get("current_user_id")  # Pass current user from frontend or auth
    if current_user_id == user_id:
        return jsonify({"error": "Cannot follow yourself"}), 400

    conn, cursor = get_db()
    try:
        # Check if already following
        cursor.execute("""
            SELECT * FROM follows
            WHERE follower_id = %s AND following_id = %s
        """, (current_user_id, user_id))
        follow = cursor.fetchone()

        if follow:
            # Unfollow
            cursor.execute("""
                DELETE FROM follows
                WHERE follower_id = %s AND following_id = %s
            """, (current_user_id, user_id))
            cursor.execute("""
                UPDATE user_profiles SET followers_count = followers_count - 1
                WHERE user_id = %s
            """, (user_id,))
            cursor.execute("""
                UPDATE user_profiles SET following_count = following_count - 1
                WHERE user_id = %s
            """, (current_user_id,))
            conn.commit()
            return jsonify({"status": "unfollowed"})

        # Create follow
        cursor.execute("""
            INSERT INTO follows (follower_id, following_id, created_at)
            VALUES (%s, %s, %s)
        """, (current_user_id, user_id, datetime.utcnow()))
        cursor.execute("""
            UPDATE user_profiles SET followers_count = followers_count + 1
            WHERE user_id = %s
        """, (user_id,))
        cursor.execute("""
            UPDATE user_profiles SET following_count = following_count + 1
            WHERE user_id = %s
        """, (current_user_id,))
        conn.commit()
        return jsonify({"status": "following"})
    finally:
        cursor.close()
        conn.close()
        
@app.route("/api/community/", methods=["GET"])       
def get_posts():
    category_id = request.args.get("category_id")
    if category_id:
        try:
            category_id = int(category_id)
        except ValueError:
            return jsonify({"error": "Invalid category_id"}), 400

    tags_filter = request.args.get("tags")
    following = request.args.get("following")
    current_user_id = request.args.get("current_user_id")

    conn, cursor = get_db(dictionary=True)
    try:
        query = """
            SELECT cp.id, cp.user_id, cp.category_id, cp.title, cp.content, cp.created_at,
                u.username,
                IFNULL(likes_count.count, 0) AS likes_count,
                IFNULL(comments_count.count, 0) AS comments_count
            FROM community_posts cp
            JOIN users u ON cp.user_id = u.id
            LEFT JOIN (
                SELECT post_id, COUNT(*) AS count
                FROM reactions
                GROUP BY post_id
            ) AS likes_count ON cp.id = likes_count.post_id
            LEFT JOIN (
                SELECT post_id, COUNT(*) AS count
                FROM post_comments
                GROUP BY post_id
            ) AS comments_count ON cp.id = comments_count.post_id
            WHERE 1=1
        """
        params = []

        if category_id:
            query += " AND cp.category_id = %s"
            params.append(category_id)

        if following == "true" and current_user_id:
            cursor.execute("SELECT following_id FROM follows WHERE follower_id = %s", (current_user_id,))
            followed_ids = [row['following_id'] for row in cursor.fetchall()]
            if followed_ids:
                placeholders = ",".join(["%s"] * len(followed_ids))
                query += f" AND cp.user_id IN ({placeholders})"
                params.extend(followed_ids)

        if tags_filter:
            tag_list = [t.strip().lower() for t in tags_filter.split(",") if t.strip()]
            if tag_list:
                placeholders = ",".join(["%s"] * len(tag_list))
                query += f"""
                    AND cp.id IN (
                        SELECT pt.post_id
                        FROM post_tags pt
                        JOIN tags t ON pt.tag_id = t.id
                        WHERE t.tag_name IN ({placeholders})
                        GROUP BY pt.post_id
                        HAVING COUNT(DISTINCT t.tag_name) = %s
                    )
                """
                params.extend(tag_list)
                params.append(len(tag_list))

        query += " ORDER BY cp.created_at DESC"
        cursor.execute(query, tuple(params))
        posts = cursor.fetchall()

        # Fetch all tags at once
        post_ids = [post['id'] for post in posts]
        if post_ids:
            placeholders = ",".join(["%s"] * len(post_ids))
            cursor.execute(f"""
                SELECT pt.post_id, t.tag_name
                FROM post_tags pt
                JOIN tags t ON pt.tag_id = t.id
                WHERE pt.post_id IN ({placeholders})
            """, tuple(post_ids))
            tag_rows = cursor.fetchall()
            tags_map = {}
            for row in tag_rows:
                tags_map.setdefault(row['post_id'], []).append(row['tag_name'])
            for post in posts:
                post['tags'] = tags_map.get(post['id'], [])

        return jsonify(posts)

    finally:
        cursor.close()
        conn.close()

@app.route("/api/comments/<int:post_id>/", methods=["GET"])
def get_comments(post_id):
    conn, cursor = get_db()
    try:
        cursor.execute("""
            SELECT c.*, u.username, u.email
            FROM comments c
            JOIN users u ON c.author_id = u.id
            WHERE c.post_id = %s AND c.parent_comment_id IS NULL
            ORDER BY created_at ASC
        """, (post_id,))
        comments = cursor.fetchall()
        return jsonify(comments)
    finally:
        cursor.close()
        conn.close()

@app.route("/api/community/", methods=["POST"])
def create_community_post():
    """
    Expects JSON:
    {
        "user_id": int,
        "category_id": int,
        "title": str,
        "content": str,
        "tags": ["tag1", "tag2"]
    }
    """
    data = request.json
    user_id = data.get("user_id")
    category_id = data.get("category_id")
    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags", [])

    if not all([user_id, category_id, title, content]):
        return jsonify({"error": "Missing required fields"}), 400

    conn, cursor = get_db(dictionary=True)
    try:
        # Insert post
        cursor.execute(
            """
            INSERT INTO community_posts (user_id, category_id, title, content)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, category_id, title, content),
        )
        post_id = cursor.lastrowid

        # Insert tags if any
        tag_ids = []
        for tag_name in tags:
            tag_name = tag_name.lower().strip()
            if not tag_name:
                continue
            # Insert new tag if it doesn't exist
            cursor.execute(
                "INSERT IGNORE INTO tags (tag_name) VALUES (%s)", (tag_name,)
            )
            # Get tag ID
            cursor.execute("SELECT id FROM tags WHERE tag_name = %s", (tag_name,))
            tag_row = cursor.fetchone()
            if tag_row:
                tag_ids.append(tag_row['id'])
        
        # Link post to tags
        for tag_id in tag_ids:
            cursor.execute(
                "INSERT INTO post_tags (post_id, tag_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE post_id=post_id",
                (post_id, tag_id)
            )

        conn.commit()

        # Fetch the created post to return
        cursor.execute(
            """
            SELECT cp.id, cp.user_id, cp.category_id, cp.title, cp.content, cp.created_at,
                   u.username
            FROM community_posts cp
            JOIN users u ON cp.user_id = u.id
            WHERE cp.id = %s
            """,
            (post_id,),
        )
        post = cursor.fetchone()

        # Attach tags
        post['tags'] = tags

        return jsonify(post), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to create post: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/community/<int:post_id>/", methods=["DELETE"])
def delete_community_post(post_id):
    data = request.json
    current_user_id = data.get("current_user_id")

    if not current_user_id:
        return jsonify({"error": "Must provide current_user_id"}), 400

    conn, cursor = get_db(dictionary=True)
    try:
        # Check user's role
        cursor.execute("""
            SELECT role 
            FROM user_roles 
            WHERE user_id = %s
            ORDER BY assigned_at DESC 
            LIMIT 1
        """, (current_user_id,))
        row = cursor.fetchone()
        role = row['role'] if row else 'user'

        if role != 'staff_admin':
            return jsonify({"error": "Unauthorized"}), 403

        # Delete the post
        cursor.execute("DELETE FROM community_posts WHERE id = %s", (post_id,))
        conn.commit()

        return jsonify({"success": True, "message": "Post deleted"})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to delete post: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
