from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import json

app = Flask(__name__, static_folder='static')
CORS(app)

DATA_FILE = 'data.json'

# Colores únicos por parapentista
COLORS = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
    "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
    "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"
]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"parapentistas": {}, "cola": []}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"parapentistas": {}, "cola": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def assign_color_and_index(data, pid):
    existing = list(data["parapentistas"].keys())
    if pid in existing:
        index = existing.index(pid)
    else:
        index = len(existing)
    color = COLORS[index % len(COLORS)]
    return index + 1, color

@app.route('/webhook/location', methods=['POST'])
def update_location():
    payload = request.json
    if not payload or "id" not in payload:
        return {"error": "Falta 'id' en el payload"}, 400

    data = load_data()
    pid = payload["id"]

    numero, color = assign_color_and_index(data, pid)

    if pid not in data["parapentistas"]:
        data["parapentistas"][pid] = {}

    data["parapentistas"][pid].update({
        "lat": payload.get("lat"),
        "lng": payload.get("lng"),
        "alt": payload.get("alt"),
        "accuracy": payload.get("accuracy"),
        "timestamp": datetime.utcnow().isoformat(),
        "numero": numero,
        "color": color
    })

    save_data(data)
    return {"status": "ok"}

@app.route('/webhook/nombre', methods=['POST'])
def update_nombre():
    payload = request.json
    if not payload or "id" not in payload or "nombre" not in payload:
        return {"error": "Falta 'id' o 'nombre'"}, 400

    data = load_data()
    pid = payload["id"]

    if pid not in data["parapentistas"]:
        data["parapentistas"][pid] = {}

    data["parapentistas"][pid]["nombre"] = payload["nombre"]

    if "siguientes" in payload:
        data["cola"] = payload["siguientes"]

    save_data(data)
    return {"status": "ok"}

@app.route('/data')
def get_data():
    try:
        return jsonify(load_data())
    except Exception as e:
        return {"error": f"Error al cargar los datos: {str(e)}"}, 500

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
