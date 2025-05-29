from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

locations = {}
lista_cola = []

@app.route('/webhook/location', methods=['POST'])
def webhook_location():
    data = request.get_json()
    if not data or 'id' not in data:
        return 'Invalid data', 400

    device_id = data['id']
    locations[device_id] = {
        'lat': data.get('lat'),
        'lng': data.get('lng'),
        'alt': data.get('alt'),
        'accuracy': data.get('accuracy'),
        'nombre': data.get('nombre'),
        'timestamp': datetime.now().isoformat()
    }
    return 'OK'

@app.route('/webhook/cola', methods=['POST'])
def webhook_cola():
    data = request.get_json()
    if not isinstance(data, list):
        return 'Invalid data', 400
    global lista_cola
    lista_cola = data
    return 'OK'

@app.route('/data')
def get_data():
    return jsonify({
        'parapentistas': locations,
        'cola': lista_cola
    })

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
