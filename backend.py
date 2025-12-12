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

mysql_pwd = os.environ.get("MYSQL_PWD")

# Database connection
config = {
    "host": host,
    "port": 3306,
    "user": "root",
    "password": mysql_pwd,  # Update with your MySQL password
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
                IFNULL(rc.likes_count, 0) AS likes_count,
                IFNULL(rc.dislikes_count, 0) AS dislikes_count,
                IFNULL(cc.comments_count, 0) AS comments_count
            FROM community_posts cp
            JOIN users u ON cp.user_id = u.id
            LEFT JOIN (
                SELECT post_id,
                    SUM(reaction_type='like') AS likes_count,
                    SUM(reaction_type='dislike') AS dislikes_count
                FROM reactions
                GROUP BY post_id
            ) AS rc ON cp.id = rc.post_id
            LEFT JOIN (
                SELECT post_id,
                    COUNT(*) AS comments_count
                FROM post_comments
                GROUP BY post_id
            ) AS cc ON cp.id = cc.post_id
            WHERE 1=1
        """

        params = []

        # Filter by category
        if category_id:
            query += " AND cp.category_id = %s"
            params.append(category_id)

        # Filter by followed authors
        if following == "true" and current_user_id:
            cursor.execute("SELECT following_id FROM follows WHERE follower_id = %s", (current_user_id,))
            followed_ids = [row['following_id'] for row in cursor.fetchall()]
            if followed_ids:
                placeholders = ",".join(["%s"] * len(followed_ids))
                query += f" AND cp.user_id IN ({placeholders})"
                params.extend(followed_ids)
            else:
                # User follows no one → return empty
                return jsonify([])

        # Filter by tags
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

            # Fetch current user's reaction
            if current_user_id:
                cursor.execute(f"""
                    SELECT post_id, reaction_type
                    FROM reactions
                    WHERE user_id = %s AND post_id IN ({placeholders})
                """, tuple([current_user_id] + post_ids))
                user_reactions_rows = cursor.fetchall()
                user_reactions = {r['post_id']: r['reaction_type'] for r in user_reactions_rows}
            else:
                user_reactions = {}

            # Attach tags and user reaction to posts
            for post in posts:
                post['tags'] = tags_map.get(post['id'], [])
                post['user_reaction'] = user_reactions.get(post['id'], None)
                post['comments_count'] = int(post.get('comments_count', 0))


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

@app.route("/api/awards/", methods=["GET"])
def list_awards():
    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute("SELECT id, category_name, award_name FROM award_categories ORDER BY award_name")
        awards = cursor.fetchall()
        return jsonify(awards)
    finally:
        cursor.close()
        conn.close()

@app.route("/api/awards/<award_table>/", methods=["GET"])
def get_award_data_by_award_table(award_table):
    if award_table not in AWARD_TABLES:
        return jsonify({"error": "Unknown award"}), 404

    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))

    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute(f"SELECT * FROM {award_table} LIMIT %s OFFSET %s", (limit, offset))
        rows = cursor.fetchall()
        return jsonify({
            "table": award_table,
            "display_name": AWARD_TABLES[award_table],
            "rows": rows,
            "limit": limit,
            "offset": offset
        })
    finally:
        cursor.close()
        conn.close()
        
@app.route("/api/community/<int:post_id>/react/", methods=["POST"])
def react_post(post_id):
    """
    Expects JSON:
    {
        "user_id": int,
        "reaction_type": "like" | "dislike"
    }
    """
    data = request.json
    user_id = data.get("user_id")
    reaction_type = data.get("reaction_type")

    if not user_id or reaction_type not in ('like', 'dislike'):
        return jsonify({"error": "User ID and valid reaction_type required"}), 400

    conn, cursor = get_db(dictionary=True)
    try:
        # Check if user already reacted
        cursor.execute("""
            SELECT id, reaction_type FROM reactions
            WHERE user_id = %s AND post_id = %s
        """, (user_id, post_id))
        existing = cursor.fetchone()

        if existing:
            if existing['reaction_type'] == reaction_type:
                # Same reaction clicked again → remove
                cursor.execute("DELETE FROM reactions WHERE id = %s", (existing['id'],))
                conn.commit()
                return jsonify({"status": "removed", "reaction_type": reaction_type})
            else:
                # Different reaction → update
                cursor.execute("""
                    UPDATE reactions
                    SET reaction_type = %s, created_at = %s
                    WHERE id = %s
                """, (reaction_type, datetime.utcnow(), existing['id']))
                conn.commit()
                return jsonify({"status": "updated", "reaction_type": reaction_type})
        else:
            # New reaction
            cursor.execute("""
                INSERT INTO reactions (user_id, post_id, reaction_type, created_at)
                VALUES (%s, %s, %s, %s)
            """, (user_id, post_id, reaction_type, datetime.utcnow()))
            conn.commit()
            return jsonify({"status": "added", "reaction_type": reaction_type})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to react: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/community/<int:post_id>/comments/", methods=["GET"])
def get_post_comments(post_id):
    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute("""
            SELECT pc.id, pc.user_id, pc.comment_text, pc.created_at,
                   u.username
            FROM post_comments pc
            JOIN users u ON pc.user_id = u.id
            WHERE pc.post_id = %s
            ORDER BY pc.created_at ASC
        """, (post_id,))
        
        comments = cursor.fetchall()
        return jsonify(comments)
    finally:
        cursor.close()
        conn.close()

@app.route("/api/community/<int:post_id>/comments/", methods=["POST"])
def create_comment(post_id):
    data = request.json
    user_id = data.get("user_id")
    comment_text = data.get("comment_text")
    
    if not user_id or not comment_text:
        return jsonify({"error": "User ID and comment text required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO post_comments (post_id, user_id, comment_text, created_at)
            VALUES (%s, %s, %s, %s)
        """, (post_id, user_id, comment_text, datetime.utcnow()))
        
        comment_id = cursor.lastrowid
        conn.commit()
        
        # Fetch the created comment with user info
        cursor.execute("""
            SELECT pc.id, pc.user_id, pc.comment_text, pc.created_at,
                   u.username
            FROM post_comments pc
            JOIN users u ON pc.user_id = u.id
            WHERE pc.id = %s
        """, (comment_id,))
        
        comment = cursor.fetchone()
        return jsonify(comment), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to create comment: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/community/<int:post_id>/comments/<int:comment_id>/", methods=["DELETE"])
def delete_comment(post_id, comment_id):
    data = request.json
    current_user_id = data.get("current_user_id")
    
    if not current_user_id:
        return jsonify({"error": "User ID required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check if user is admin or comment author
        cursor.execute("""
            SELECT role FROM user_roles 
            WHERE user_id = %s
            ORDER BY assigned_at DESC 
            LIMIT 1
        """, (current_user_id,))
        
        role_row = cursor.fetchone()
        role = role_row['role'] if role_row else 'user'
        
        cursor.execute("""
            SELECT user_id FROM post_comments WHERE id = %s
        """, (comment_id,))
        
        comment = cursor.fetchone()
        
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Allow deletion if user is admin or comment author
        if role == 'staff_admin' or comment['user_id'] == current_user_id:
            cursor.execute("DELETE FROM post_comments WHERE id = %s", (comment_id,))
            conn.commit()
            return jsonify({"success": True, "message": "Comment deleted"})
        else:
            return jsonify({"error": "Unauthorized"}), 403
            
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to delete comment: {e}"}), 500
    finally:
        cursor.close()
        conn.close()
        
@app.route("/api/community/<int:post_id>/bookmark/", methods=["POST"])
def toggle_bookmark(post_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM bookmarks WHERE user_id = %s AND post_id = %s",
            (user_id, post_id)
        )
        bookmark = cursor.fetchone()

        if bookmark:
            cursor.execute(
                "DELETE FROM bookmarks WHERE user_id = %s AND post_id = %s",
                (user_id, post_id)
            )
            conn.commit()
            return jsonify({"status": "removed"})
        else:
            cursor.execute(
                "INSERT INTO bookmarks (user_id, post_id, created_at) VALUES (%s, %s, %s)",
                (user_id, post_id, datetime.utcnow())
            )
            conn.commit()
            return jsonify({"status": "added"})
    finally:
        cursor.close()
        conn.close()


@app.route("/api/community/bookmarks/", methods=["GET"])
def get_bookmarked_posts():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify([])

    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT cp.*, 
                   IFNULL(rc.likes_count, 0) AS likes_count,
                   IFNULL(rc.dislikes_count, 0) AS dislikes_count,
                   IFNULL(cc.comments_count, 0) AS comments_count
            FROM community_posts cp
            JOIN bookmarks b ON b.post_id = cp.id
            LEFT JOIN (
                SELECT post_id, 
                       SUM(reaction_type='like') AS likes_count,
                       SUM(reaction_type='dislike') AS dislikes_count
                FROM reactions
                GROUP BY post_id
            ) rc ON cp.id = rc.post_id
            LEFT JOIN (
                SELECT post_id, COUNT(*) AS comments_count
                FROM post_comments
                GROUP BY post_id
            ) cc ON cp.id = cc.post_id
            WHERE b.user_id = %s
            ORDER BY b.created_at DESC
            """,
            (user_id,)
        )
        posts = cursor.fetchall()
        return jsonify(posts)
    finally:
        cursor.close()
        conn.close()


# GROUPS ROUTES
@app.route("/api/groups/", methods=["GET"])
def get_groups():
    """Get all groups or filter by user membership"""
    user_id = request.args.get("user_id")
    
    conn, cursor = get_db(dictionary=True)
    try:
        if user_id:
            # Get groups where user is a member
            cursor.execute("""
                SELECT dg.*, 
                       u.username as creator_username,
                       gm.role as user_role,
                       COUNT(DISTINCT gm2.id) as member_count,
                       COUNT(DISTINCT gp.id) as post_count
                FROM discussion_groups dg
                JOIN users u ON dg.created_by = u.id
                LEFT JOIN group_memberships gm ON dg.id = gm.group_id AND gm.user_id = %s
                LEFT JOIN group_memberships gm2 ON dg.id = gm2.group_id
                LEFT JOIN group_posts gp ON dg.id = gp.group_id
                WHERE gm.user_id = %s
                GROUP BY dg.id
                ORDER BY dg.created_at DESC
            """, (user_id, user_id))
        else:
            # Get all public groups
            cursor.execute("""
                SELECT dg.*, 
                       u.username as creator_username,
                       COUNT(DISTINCT gm.id) as member_count,
                       COUNT(DISTINCT gp.id) as post_count
                FROM discussion_groups dg
                JOIN users u ON dg.created_by = u.id
                LEFT JOIN group_memberships gm ON dg.id = gm.group_id
                LEFT JOIN group_posts gp ON dg.id = gp.group_id
                GROUP BY dg.id
                ORDER BY dg.created_at DESC
            """)
        
        groups = cursor.fetchall()
        return jsonify(groups)
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/", methods=["POST"])
def create_group():
    """Create a new discussion group"""
    data = request.json
    name = data.get("name")
    description = data.get("description")
    created_by = data.get("created_by")
    
    if not all([name, created_by]):
        return jsonify({"error": "Name and creator required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check if user is admin
        cursor.execute("""
            SELECT role FROM user_roles 
            WHERE user_id = %s
            ORDER BY assigned_at DESC 
            LIMIT 1
        """, (created_by,))
        role_row = cursor.fetchone()
        user_role = role_row['role'] if role_row else 'user'
        
        # Create group
        cursor.execute("""
            INSERT INTO discussion_groups (name, description, created_by, created_at)
            VALUES (%s, %s, %s, %s)
        """, (name, description, created_by, datetime.utcnow()))
        
        group_id = cursor.lastrowid
        
        # Add creator as admin (or keep admin role if they're staff_admin)
        member_role = 'admin' if user_role != 'staff_admin' else 'admin'
        cursor.execute("""
            INSERT INTO group_memberships (group_id, user_id, role, joined_at)
            VALUES (%s, %s, %s, %s)
        """, (group_id, created_by, member_role, datetime.utcnow()))
        
        conn.commit()
        
        # Fetch created group
        cursor.execute("""
            SELECT dg.*, u.username as creator_username,
                   0 as member_count, 0 as post_count
            FROM discussion_groups dg
            JOIN users u ON dg.created_by = u.id
            WHERE dg.id = %s
        """, (group_id,))
        
        group = cursor.fetchone()
        return jsonify(group), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to create group: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/", methods=["GET"])
def get_group(group_id):
    """Get detailed group information"""
    user_id = request.args.get("user_id")
    
    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute("""
            SELECT dg.*, 
                   u.username as creator_username,
                   COUNT(DISTINCT gm.id) as member_count
            FROM discussion_groups dg
            JOIN users u ON dg.created_by = u.id
            LEFT JOIN group_memberships gm ON dg.id = gm.group_id
            WHERE dg.id = %s
            GROUP BY dg.id
        """, (group_id,))
        
        group = cursor.fetchone()
        
        if not group:
            return jsonify({"error": "Group not found"}), 404
        
        # Check user's membership status
        if user_id:
            cursor.execute("""
                SELECT role FROM group_memberships
                WHERE group_id = %s AND user_id = %s
            """, (group_id, user_id))
            membership = cursor.fetchone()
            group['user_role'] = membership['role'] if membership else None
            group['is_member'] = membership is not None
        else:
            group['user_role'] = None
            group['is_member'] = False
        
        return jsonify(group)
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/", methods=["DELETE"])
def delete_group(group_id):
    """Delete a group (creator, group admin, or staff admin only)"""
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check if user is staff admin
        cursor.execute("""
            SELECT role FROM user_roles 
            WHERE user_id = %s
            ORDER BY assigned_at DESC 
            LIMIT 1
        """, (user_id,))
        role_row = cursor.fetchone()
        is_staff_admin = role_row and role_row['role'] == 'staff_admin'
        
        # Check if user is group creator or admin
        cursor.execute("""
            SELECT created_by FROM discussion_groups WHERE id = %s
        """, (group_id,))
        group = cursor.fetchone()
        
        if not group:
            return jsonify({"error": "Group not found"}), 404
        
        cursor.execute("""
            SELECT role FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        membership = cursor.fetchone()
        
        is_group_admin = membership and membership['role'] == 'admin'
        is_creator = group['created_by'] == user_id
        
        if not (is_staff_admin or is_group_admin or is_creator):
            return jsonify({"error": "Unauthorized"}), 403
        
        # Delete group
        cursor.execute("DELETE FROM discussion_groups WHERE id = %s", (group_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "Group deleted"})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to delete group: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/join/", methods=["POST"])
def join_group(group_id):
    """Join a group as a member"""
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check if already a member
        cursor.execute("""
            SELECT id FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        if cursor.fetchone():
            return jsonify({"error": "Already a member"}), 400
        
        # Check if user is staff admin - they keep admin privileges
        cursor.execute("""
            SELECT role FROM user_roles 
            WHERE user_id = %s
            ORDER BY assigned_at DESC 
            LIMIT 1
        """, (user_id,))
        role_row = cursor.fetchone()
        is_staff_admin = role_row and role_row['role'] == 'staff_admin'
        
        member_role = 'admin' if is_staff_admin else 'member'
        
        cursor.execute("""
            INSERT INTO group_memberships (group_id, user_id, role, joined_at)
            VALUES (%s, %s, %s, %s)
        """, (group_id, user_id, member_role, datetime.utcnow()))
        
        conn.commit()
        return jsonify({"success": True, "role": member_role})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to join group: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/leave/", methods=["POST"])
def leave_group(group_id):
    """Leave a group"""
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check if user is the creator
        cursor.execute("""
            SELECT created_by FROM discussion_groups WHERE id = %s
        """, (group_id,))
        group = cursor.fetchone()
        
        if group and group['created_by'] == user_id:
            return jsonify({"error": "Group creator cannot leave. Delete the group instead."}), 400
        
        cursor.execute("""
            DELETE FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        conn.commit()
        return jsonify({"success": True})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to leave group: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/members/", methods=["GET"])
def get_group_members(group_id):
    """Get all members of a group"""
    conn, cursor = get_db(dictionary=True)
    try:
        cursor.execute("""
            SELECT gm.*, u.username, u.email
            FROM group_memberships gm
            JOIN users u ON gm.user_id = u.id
            WHERE gm.group_id = %s
            ORDER BY gm.joined_at DESC
        """, (group_id,))
        
        members = cursor.fetchall()
        return jsonify(members)
    finally:
        cursor.close()
        conn.close()


# GROUP POSTS ROUTES
@app.route("/api/groups/<int:group_id>/posts/", methods=["GET"])
def get_group_posts(group_id):
    """Get all posts in a group (members only)"""
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 401
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check membership
        cursor.execute("""
            SELECT id FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        if not cursor.fetchone():
            return jsonify({"error": "Not a member of this group"}), 403
        
        # Get posts
        cursor.execute("""
            SELECT gp.*, u.username,
                   IFNULL(likes.count, 0) as likes_count,
                   IFNULL(dislikes.count, 0) as dislikes_count,
                   IFNULL(comments.count, 0) as comments_count
            FROM group_posts gp
            JOIN users u ON gp.user_id = u.id
            LEFT JOIN (
                SELECT post_id, COUNT(*) as count
                FROM reactions_group
                WHERE reaction_type = 'like' AND post_id IS NOT NULL
                GROUP BY post_id
            ) as likes ON gp.id = likes.post_id
            LEFT JOIN (
                SELECT post_id, COUNT(*) as count
                FROM reactions_group
                WHERE reaction_type = 'dislike' AND post_id IS NOT NULL
                GROUP BY post_id
            ) as dislikes ON gp.id = dislikes.post_id
            LEFT JOIN (
                SELECT post_id, COUNT(*) as count
                FROM group_post_comments
                GROUP BY post_id
            ) as comments ON gp.id = comments.post_id
            WHERE gp.group_id = %s
            ORDER BY gp.created_at DESC
        """, (group_id,))
        
        posts = cursor.fetchall()
        
        # Check user's reactions
        post_ids = [p['id'] for p in posts]
        if post_ids:
            placeholders = ",".join(["%s"] * len(post_ids))
            cursor.execute(f"""
                SELECT post_id, reaction_type 
                FROM reactions_group
                WHERE user_id = %s AND post_id IN ({placeholders})
            """, tuple([user_id] + post_ids))
            
            reactions = {r['post_id']: r['reaction_type'] for r in cursor.fetchall()}
            
            for post in posts:
                post['user_reaction'] = reactions.get(post['id'])
        
        return jsonify(posts)
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/posts/", methods=["POST"])
def create_group_post(group_id):
    """Create a post in a group (members only)"""
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags", [])
    
    if not all([user_id, title, content]):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check membership
        cursor.execute("""
            SELECT id FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        if not cursor.fetchone():
            return jsonify({"error": "Not a member of this group"}), 403
        
        # Create post
        cursor.execute("""
            INSERT INTO group_posts (group_id, user_id, title, content, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (group_id, user_id, title, content, datetime.utcnow()))
        
        post_id = cursor.lastrowid
        
        # Handle tags
        tag_ids = []
        for tag_name in tags:
            tag_name = tag_name.lower().strip()
            if not tag_name:
                continue
            cursor.execute("INSERT IGNORE INTO tags (tag_name) VALUES (%s)", (tag_name,))
            cursor.execute("SELECT id FROM tags WHERE tag_name = %s", (tag_name,))
            tag_row = cursor.fetchone()
            if tag_row:
                tag_ids.append(tag_row['id'])
        
        for tag_id in tag_ids:
            cursor.execute("""
                INSERT INTO post_tags_group (post_id, tag_id) 
                VALUES (%s, %s) ON DUPLICATE KEY UPDATE post_id=post_id
            """, (post_id, tag_id))
        
        conn.commit()
        
        # Fetch created post
        cursor.execute("""
            SELECT gp.*, u.username,
                   0 as likes_count, 0 as dislikes_count, 0 as comments_count
            FROM group_posts gp
            JOIN users u ON gp.user_id = u.id
            WHERE gp.id = %s
        """, (post_id,))
        
        post = cursor.fetchone()
        post['tags'] = tags
        return jsonify(post), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to create post: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/posts/<int:post_id>/", methods=["DELETE"])
def delete_group_post(group_id, post_id):
    """Delete a group post (author, group admin, or staff admin)"""
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check if staff admin
        cursor.execute("""
            SELECT role FROM user_roles 
            WHERE user_id = %s
            ORDER BY assigned_at DESC 
            LIMIT 1
        """, (user_id,))
        role_row = cursor.fetchone()
        is_staff_admin = role_row and role_row['role'] == 'staff_admin'
        
        # Check post ownership
        cursor.execute("SELECT user_id FROM group_posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            return jsonify({"error": "Post not found"}), 404
        
        # Check group admin
        cursor.execute("""
            SELECT role FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        membership = cursor.fetchone()
        is_group_admin = membership and membership['role'] == 'admin'
        
        if not (is_staff_admin or is_group_admin or post['user_id'] == user_id):
            return jsonify({"error": "Unauthorized"}), 403
        
        cursor.execute("DELETE FROM group_posts WHERE id = %s", (post_id,))
        conn.commit()
        
        return jsonify({"success": True})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to delete post: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/posts/<int:post_id>/react/", methods=["POST"])
def react_to_group_post(group_id, post_id):
    """Like or dislike a group post"""
    data = request.json
    user_id = data.get("user_id")
    reaction_type = data.get("reaction_type")  # 'like' or 'dislike'
    
    if not user_id or reaction_type not in ['like', 'dislike']:
        return jsonify({"error": "Invalid request"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check membership
        cursor.execute("""
            SELECT id FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        if not cursor.fetchone():
            return jsonify({"error": "Not a member"}), 403
        
        # Check existing reaction
        cursor.execute("""
            SELECT id, reaction_type FROM reactions_group
            WHERE user_id = %s AND post_id = %s
        """, (user_id, post_id))
        
        existing = cursor.fetchone()
        
        if existing:
            if existing['reaction_type'] == reaction_type:
                # Remove reaction
                cursor.execute("""
                    DELETE FROM reactions_group
                    WHERE user_id = %s AND post_id = %s
                """, (user_id, post_id))
                conn.commit()
                return jsonify({"reaction": None})
            else:
                # Update reaction
                cursor.execute("""
                    UPDATE reactions_group 
                    SET reaction_type = %s
                    WHERE user_id = %s AND post_id = %s
                """, (reaction_type, user_id, post_id))
                conn.commit()
                return jsonify({"reaction": reaction_type})
        else:
            # Create new reaction
            cursor.execute("""
                INSERT INTO reactions_group (user_id, post_id, reaction_type, created_at)
                VALUES (%s, %s, %s, %s)
            """, (user_id, post_id, reaction_type, datetime.utcnow()))
            conn.commit()
            return jsonify({"reaction": reaction_type})
            
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to react: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


# GROUP COMMENTS ROUTES
@app.route("/api/groups/<int:group_id>/posts/<int:post_id>/comments/", methods=["GET"])
def get_group_post_comments(group_id, post_id):
    """Get comments for a group post"""
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 401
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check membership
        cursor.execute("""
            SELECT id FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        if not cursor.fetchone():
            return jsonify({"error": "Not a member"}), 403
        
        cursor.execute("""
            SELECT gpc.*, u.username,
                   IFNULL(likes.count, 0) as likes_count,
                   IFNULL(dislikes.count, 0) as dislikes_count
            FROM group_post_comments gpc
            JOIN users u ON gpc.user_id = u.id
            LEFT JOIN (
                SELECT comment_id, COUNT(*) as count
                FROM reactions_group
                WHERE reaction_type = 'like' AND comment_id IS NOT NULL
                GROUP BY comment_id
            ) as likes ON gpc.id = likes.comment_id
            LEFT JOIN (
                SELECT comment_id, COUNT(*) as count
                FROM reactions_group
                WHERE reaction_type = 'dislike' AND comment_id IS NOT NULL
                GROUP BY comment_id
            ) as dislikes ON gpc.id = dislikes.comment_id
            WHERE gpc.post_id = %s
            ORDER BY gpc.created_at ASC
        """, (post_id,))
        
        comments = cursor.fetchall()
        
        # Check user reactions
        comment_ids = [c['id'] for c in comments]
        if comment_ids:
            placeholders = ",".join(["%s"] * len(comment_ids))
            cursor.execute(f"""
                SELECT comment_id, reaction_type
                FROM reactions_group
                WHERE user_id = %s AND comment_id IN ({placeholders})
            """, tuple([user_id] + comment_ids))
            
            reactions = {r['comment_id']: r['reaction_type'] for r in cursor.fetchall()}
            
            for comment in comments:
                comment['user_reaction'] = reactions.get(comment['id'])
        
        return jsonify(comments)
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/posts/<int:post_id>/comments/", methods=["POST"])
def create_group_comment(group_id, post_id):
    """Create a comment on a group post"""
    data = request.json
    user_id = data.get("user_id")
    comment_text = data.get("comment_text")
    
    if not user_id or not comment_text:
        return jsonify({"error": "Missing required fields"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check membership
        cursor.execute("""
            SELECT id FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        if not cursor.fetchone():
            return jsonify({"error": "Not a member"}), 403
        
        cursor.execute("""
            INSERT INTO group_post_comments (post_id, user_id, comment_text, created_at)
            VALUES (%s, %s, %s, %s)
        """, (post_id, user_id, comment_text, datetime.utcnow()))
        
        comment_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute("""
            SELECT gpc.*, u.username,
                   0 as likes_count, 0 as dislikes_count
            FROM group_post_comments gpc
            JOIN users u ON gpc.user_id = u.id
            WHERE gpc.id = %s
        """, (comment_id,))
        
        comment = cursor.fetchone()
        return jsonify(comment), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to create comment: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/posts/<int:post_id>/comments/<int:comment_id>/", methods=["DELETE"])
def delete_group_comment(group_id, post_id, comment_id):
    """Delete a group comment (author, group admin, or staff admin)"""
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check if staff admin
        cursor.execute("""
            SELECT role FROM user_roles 
            WHERE user_id = %s
            ORDER BY assigned_at DESC 
            LIMIT 1
        """, (user_id,))
        role_row = cursor.fetchone()
        is_staff_admin = role_row and role_row['role'] == 'staff_admin'
        
        # Check comment ownership
        cursor.execute("""
            SELECT user_id FROM group_post_comments WHERE id = %s
        """, (comment_id,))
        comment = cursor.fetchone()
        
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Check group admin
        cursor.execute("""
            SELECT role FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        membership = cursor.fetchone()
        is_group_admin = membership and membership['role'] == 'admin'
        
        if not (is_staff_admin or is_group_admin or comment['user_id'] == user_id):
            return jsonify({"error": "Unauthorized"}), 403
        
        cursor.execute("DELETE FROM group_post_comments WHERE id = %s", (comment_id,))
        conn.commit()
        
        return jsonify({"success": True})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to delete comment: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/api/groups/<int:group_id>/posts/<int:post_id>/comments/<int:comment_id>/react/", methods=["POST"])
def react_to_group_comment(group_id, post_id, comment_id):
    """Like or dislike a group comment"""
    data = request.json
    user_id = data.get("user_id")
    reaction_type = data.get("reaction_type")
    
    if not user_id or reaction_type not in ['like', 'dislike']:
        return jsonify({"error": "Invalid request"}), 400
    
    conn, cursor = get_db(dictionary=True)
    try:
        # Check membership
        cursor.execute("""
            SELECT id FROM group_memberships
            WHERE group_id = %s AND user_id = %s
        """, (group_id, user_id))
        
        if not cursor.fetchone():
            return jsonify({"error": "Not a member"}), 403
        
        # Check existing reaction
        cursor.execute("""
            SELECT id, reaction_type FROM reactions_group
            WHERE user_id = %s AND comment_id = %s
        """, (user_id, comment_id))
        
        existing = cursor.fetchone()
        
        if existing:
            if existing['reaction_type'] == reaction_type:
                cursor.execute("""
                    DELETE FROM reactions_group
                    WHERE user_id = %s AND comment_id = %s
                """, (user_id, comment_id))
                conn.commit()
                return jsonify({"reaction": None})
            else:
                cursor.execute("""
                    UPDATE reactions_group 
                    SET reaction_type = %s
                    WHERE user_id = %s AND comment_id = %s
                """, (reaction_type, user_id, comment_id))
                conn.commit()
                return jsonify({"reaction": reaction_type})
        else:
            cursor.execute("""
                INSERT INTO reactions_group (user_id, comment_id, reaction_type, created_at)
                VALUES (%s, %s, %s, %s)
            """, (user_id, comment_id, reaction_type, datetime.utcnow()))
            conn.commit()
            return jsonify({"reaction": reaction_type})
            
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Failed to react: {e}"}), 500
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)
