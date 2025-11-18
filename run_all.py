#!/usr/bin/env python3
import subprocess
import os
import platform

# Get the current directory (assuming script is run from PrizeTalk)
current_dir = os.getcwd()

def run_command(command, cwd=None, shell=True):
    """Run a command."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=shell, cwd=cwd or current_dir)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        exit(1)

# Step 1: Load the database
if os.path.exists('/mnt/c') and 'microsoft' in platform.platform().lower():
    # Running in WSL on Windows, use PowerShell to run the Python script
    project_dir_windows = current_dir.replace('/mnt/c', 'C:')
    run_command(f'powershell.exe -Command "cd \\"{project_dir_windows}\\"; python prizetalk_db.py"')
else:
    # On native Linux/macOS or other, run directly
    run_command("python prizetalk_db.py")

# Step 2: Start the backend server in background
print("Starting backend server...")
subprocess.Popen(['python3', 'backend.py'], cwd=current_dir)

# Step 3: Start the Vue development server
vue_dir = os.path.join(current_dir, "PrizeTalk_Code")
run_command("npm run dev", cwd=vue_dir)