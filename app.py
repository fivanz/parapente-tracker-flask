from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo  # ✅ Importado para la zona horaria de Colombia
from waitress import serve

app = Flask(__name__, static_folder='static')
CORS(app)

STORE_PATH = 'data/store.json'

# Inicializar almacenamiento
def init_store():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.isfile(STORE_PATH):
        with open(STORE_PATH, 'w') as f:
            json.dump({"parapentistas": {}, "cola": []}, f)

# Cargar datos
def load_data():
    with open(STORE_PATH, 'r') as f:
        return json.load(f)

# Guardar datos
def save_data(data):
    with open(STORE_PATH, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify({
        "parapentistas": data.get("parapentistas", {}),
        "cola": data.get("cola", [])
    })

@app.route('/webhook/location', methods=['POST'])
def update_location():
    payload = request.json
    pid = payload.get("id")

    if not pid:
        return {"error": "ID requerido"}, 400

    data = load_data()
    data["parapentistas"].setdefault(pid, {})
    data["parapentistas"][pid].update({
        "lat": payload.get("lat"),
        "lng": payload.get("lng"),
        "alt": payload.get("alt"),
        "accuracy": payload.get("accuracy"),
        "timestamp": datetime.now(ZoneInfo("America/Bogota")).isoformat()  # ✅ Zona horaria Colombia
    })

    save_data(data)
    return {"status": "ok"}

@app.route('/webhook/nombre', methods=['POST'])
def update_nombre():
    payload = request.json
    pid = payload.get("id")
    nombre = payload.get("nombre")
    cola = payload.get("siguientes", [])

    data = load_data()

    if pid and nombre:
        data["parapentistas"].setdefault(pid, {})
        data["parapentistas"][pid]["nombre"] = nombre

    if cola:
        data["cola"] = cola

    save_data(data)
    return {"status": "ok"}

if __name__ == '__main__':
    init_store()
    serve(app, host='0.0.0.0', port=8000)
