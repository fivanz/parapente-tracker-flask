# ... (importaciones y configuración inicial)

COLORS = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
    "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
    "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"
]

def assign_color_and_index(data, pid):
    existing = list(data["parapentistas"].keys())
    index = existing.index(pid) if pid in existing else len(existing)
    color = COLORS[index % len(COLORS)]
    return index + 1, color

@app.route('/webhook/location', methods=['POST'])
def update_location():
    payload = request.json
    data = load_data()
    pid = payload.get("id")
    if not pid:
        return {"error": "ID requerido"}, 400

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
