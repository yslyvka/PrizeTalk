#!/usr/bin/env python3
import subprocess
import os
import sys
import mysql.connector
import getpass

current_dir = os.getcwd()
vue_dir = os.path.join(current_dir, "PrizeTalk_Code")
BACKEND_PORT = 3000

def run_command(cmd, cwd=None, env=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, cwd=cwd or current_dir, env=env, shell=True)
    if result.returncode != 0:
        print("Error:", cmd)
        sys.exit(1)

def database_initialized(password):
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=password,
            database="prizetalk"
        )
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        cur.close()
        conn.close()
        return len(tables) > 0
    except mysql.connector.Error:
        return False

# ---- Ask for MySQL password ----
mysql_pwd = getpass.getpass("Enter MySQL root password: ")

# load database only if needed
if database_initialized(mysql_pwd):
    print("✔ Database exists — skipping prizetalk_db.py")
else:
    print("⚙ Database not found — running prizetalk_db.py ...")
    env_db = os.environ.copy()
    env_db["MYSQL_PWD"] = mysql_pwd
    run_command("python3 prizetalk_db.py", env=env_db)

# start backend using flask
env_backend = os.environ.copy()
env_backend["FLASK_APP"] = "backend.py"
env_backend["FLASK_ENV"] = "development"
env_backend["MYSQL_PWD"] = mysql_pwd

subprocess.Popen(
    f"python3 -m flask run --port {BACKEND_PORT}",
    cwd=current_dir,
    env=env_backend,
    shell=True
)


env_frontend = os.environ.copy()
env_frontend["VITE_API_PROXY_TARGET"] = f"http://localhost:{BACKEND_PORT}"
run_command("npm run dev", cwd=vue_dir, env=env_frontend)
