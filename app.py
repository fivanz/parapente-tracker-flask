from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

STORE_FILE = 'store.json'

# Cargar datos desde archivo
def load_data():
    if not os.path.exists(STORE_FILE):
        return {}
    try:
        with open(STORE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

# Guardar datos
def save_data(data):
    with open(STORE_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/webhook/location', methods=['POST'])
def webhook():
    incoming = request.get_json(force=True)
    if not incoming:
        return 'No data received', 400

    data = load_data()
    now = time.time()

    point = {
        'id': str(incoming.get('id', '0')),
        'lat': incoming.get('lat'),
        'lon': incoming.get('lon'),
        'alt': incoming.get('alt'),
        'acc': incoming.get('acc'),
        'name': incoming.get('name', 'Sin nombre'),
        'timestamp': now
    }

    data[point['id']] = point
    save_data(data)
    return 'OK', 200

@app.route('/data')
def get_data():
    data = load_data()
    now = time.time()
    active = {}

    for k, v in data.items():
        if now - v.get('timestamp', 0) < 5 * 60:
            active[k] = v

    return jsonify(active)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
