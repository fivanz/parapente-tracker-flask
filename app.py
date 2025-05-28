from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

DATA_FILE = 'data.json'

# Función para cargar datos desde archivo JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"parapentistas": {}, "cola": []}
    return {"parapentistas": {}, "cola": []}

# Función para guardar datos en archivo JSON
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Ruta para recibir datos desde los dispositivos GPS (webhook)
@app.route('/webhook', methods=['POST'])
def webhook():
    content = request.json
    required_keys = ['id', 'lat', 'lng']
    
    if not content or not all(k in content for k in required_keys):
        return jsonify({'error': 'Datos incompletos'}), 400

    data = load_data()
    p_id = str(content['id'])
    data['parapentistas'][p_id] = {
        'lat': content['lat'],
        'lng': content['lng'],
        'nombre': content.get('nombre', p_id)
    }

    save_data(data)
    return jsonify({'status': 'ok'})

# Ruta para actualizar la cola manualmente (opcional)
@app.route('/cola', methods=['POST'])
def actualizar_cola():
    content = request.json
    if not content or 'cola' not in content or not isinstance(content['cola'], list):
        return jsonify({'error': 'Formato incorrecto'}), 400

    data = load_data()
    data['cola'] = content['cola']
    save_data(data)
    return jsonify({'status': 'cola actualizada'})

# Ruta para servir los datos al frontend
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

# Ruta para servir el archivo HTML
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Ruta para servir otros archivos estáticos (JS, CSS, etc.)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
