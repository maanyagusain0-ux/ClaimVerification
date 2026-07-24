import subprocess
import sys
import os
import webbrowser
import time

# Path to app.py
app_path = os.path.join(os.path.dirname(__file__), "app.py")

# Start Streamlit
subprocess.Popen([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    app_path,
    "--server.headless=true"
])

# Give Streamlit a few seconds to start
time.sleep(5)

# Open browser automatically
webbrowser.open("http://localhost:8501")