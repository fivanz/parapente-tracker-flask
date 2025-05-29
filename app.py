from flask import Flask, request, jsonify, send_from_directory, render_template
from datetime import datetime
import threading

app = Flask(__name__)

# Almacenamiento en memoria
parapentistas = {}
cola_vuelos = []

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/webhook/location", methods=["POST"])
def recibir_datos():
    data = request.get_json()
    if not data or "id" not in data or "lat" not in data or "lng" not in data:
        return "Faltan datos obligatorios", 400

    id_ = str(data["id"])
    parapentistas[id_] = {
        "lat": data["lat"],
        "lng": data["lng"],
        "alt": data.get("alt"),
        "accuracy": data.get("accuracy"),
        "nombre": data.get("nombre", "Sin nombre"),
        "timestamp": datetime.now().isoformat()
    }

    return "OK", 200

@app.route("/webhook/cola", methods=["POST"])
def agregar_a_cola():
    data = request.get_json()
    nombre = data.get("nombre")
    if not nombre:
        return "Nombre requerido", 400
    cola_vuelos.append(nombre)
    if len(cola_vuelos) > 20:
        cola_vuelos.pop(0)
    return "Agregado", 200

@app.route("/data")
def data():
    return jsonify({
        "parapentistas": parapentistas,
        "cola": cola_vuelos
    })

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

def limpiar_parapentistas():
    while True:
        import time
        time.sleep(60)
        ahora = datetime.now()
        expirados = [
            id_ for id_, p in parapentistas.items()
            if (ahora - datetime.fromisoformat(p["timestamp"])).total_seconds() > 180
        ]
        for id_ in expirados:
            del parapentistas[id_]

# Hilo para limpieza automática (opcional)
threading.Thread(target=limpiar_parapentistas, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
