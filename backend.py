from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import platform
import os

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
    "password": "",  # Update with your MySQL password
    "database": "prizetalk",
}


def get_db(dictionary=False):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=dictionary)
    return connection, cursor

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
            'kind': 'staff',  # Staff dashboard is the only implemented flow for now
            'account': {
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
            },
            'staff': {
                'role': role,
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
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)