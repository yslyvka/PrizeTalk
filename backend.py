from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import platform
import os

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
    "password": "Ternopil@2007",  # Update with your MySQL password
    "database": "prizetalk",
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password required'}), 400
    
    cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    
    if result and bcrypt.checkpw(password.encode(), result[0].encode()):
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    
    if not all([first_name, last_name, email, password]):
        return jsonify({'success': False, 'message': 'All fields required'}), 400
    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    username = f"{first_name} {last_name}"
    
    try:
        cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)", (username, hashed, email))
        conn.commit()
        return jsonify({'success': True})
    except mysql.connector.IntegrityError:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)