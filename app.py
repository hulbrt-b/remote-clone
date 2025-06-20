from flask import Flask, render_template, request, jsonify
import threading
import subprocess
import time
import json
import os
from datetime import datetime
from config import SERVERS

app = Flask(__name__)
HISTORY_FILE = "logs/history.json"
RUNNING_TASKS = {}  # track running jobs and their progress

os.makedirs("logs", exist_ok=True)
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump({}, f)

def run_clone(server_name, remote_host, destination):
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history = {}

    try:
        cmd = f"ssh root@{remote_host} 'dd if=/dev/sda bs=4M status=progress' | dd of={destination} bs=4M status=progress"
        process = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        RUNNING_TASKS[server_name] = {"status": "RUNNING", "progress": 0}

        for line in process.stderr:
            if "bytes" in line:
                try:
                    # crude progress parse (can improve with pv)
                    bytes_done = int(line.split()[0])
                    RUNNING_TASKS[server_name]["progress"] = bytes_done
                except:
                    continue

        process.wait()
        result = "SUCCESS" if process.returncode == 0 else "FAILURE"

    except Exception as e:
        result = "FAILURE"

    duration = round(time.time() - start_time)
    with open(HISTORY_FILE, "r+") as f:
        try:
            history = json.load(f)
        except:
            history = {}
        history[server_name] = {
            "last_run": timestamp,
            "duration": duration,
            "status": result
        }
        f.seek(0)
        json.dump(history, f, indent=2)

    RUNNING_TASKS[server_name] = {"status": result, "progress": 0}

@app.route("/")
def index():
    with open(HISTORY_FILE) as f:
        history_data = json.load(f)

    servers = []
    for name, cfg in SERVERS.items():
        h = history_data.get(name, {})
        servers.append({
            "name": name,
            "destination": cfg["disk"],
            "last_run": h.get("last_run"),
            "duration": h.get("duration"),
            "status": h.get("status"),
        })

    return render_template("index.html", servers=servers)

@app.route("/start-multiple", methods=["POST"])
def start_multiple():
    data = request.get_json()
    selected_servers = data.get("servers", [])
    task_map = {}

    for server_name in selected_servers:
        if server_name in RUNNING_TASKS and RUNNING_TASKS[server_name]["status"] == "RUNNING":
            continue  # already running

        config = SERVERS.get(server_name)
        if not config:
            continue

        thread = threading.Thread(
            target=run_clone,
            args=(server_name, config["host"], config["disk"]),
            daemon=True
        )
        thread.start()
        task_map[server_name] = "started"

    return jsonify(task_map)

@app.route("/status/<server_name>")
def check_status(server_name):
    status = RUNNING_TASKS.get(server_name, {"status": "Idle", "progress": 0})
    return jsonify(status)

if __name__ == "__main__":
    app.run(debug=True)
