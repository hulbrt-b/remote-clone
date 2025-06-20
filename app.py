from flask import Flask, render_template, jsonify, request
from tasks import clone_disk, get_status
import json
import os

app = Flask(__name__)

HISTORY_FILE = "logs/history.json"

@app.route('/')
def index():
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    return render_template('index.html', history=history)

@app.route('/start', methods=['POST'])
def start_clone():
    source = request.form['source']
    destination = request.form['destination']
    task = clone_disk.apply_async(args=[source, destination])
    return jsonify({'task_id': task.id})

@app.route('/status/<task_id>')
def task_status(task_id):
    return jsonify(get_status(task_id))

if __name__ == '__main__':
    app.run(debug=True)

