import subprocess
import webbrowser
import time
import sys

subprocess.Popen(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.headless=true"
    ]
)

time.sleep(2)

webbrowser.open(
    "http://localhost:8501"
)