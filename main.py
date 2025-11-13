from flask import Flask, request, jsonify
import json
import os
import math

# Cargar los datos del archivo JSON
with open('db/koox_stops_routes.json') as f:
    stops_data = json.load(f)

# Crear la app Flask
app = Flask(__name__)

# Función para calcular la distancia entre dos puntos geográficos (en km)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en kilómetros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Retorna la distancia en kilómetros

# Endpoint para obtener todas las paradas
@app.route("/stops", methods=["GET"])
def get_stops():
    return jsonify({"ok": True, "code_http": 200, "body": stops_data})

# Endpoint para obtener una parada específica por nombre
@app.route("/stops/<stop_name>", methods=["GET"])
def get_stop(stop_name):
    stop = next((s for s in stops_data if s["Stop_Name"].lower() == stop_name.lower()), None)
    if not stop:
        return jsonify({"ok": False, "code_http": 404}), 404
    return jsonify({"ok": True, "code_http": 200, "body": stop})

# Endpoint para crear una nueva parada
@app.route("/stops", methods=["POST"])
def create_stop():
    stop = request.get_json()
    # Verificar si la parada ya existe
    if any(s["Stop_Name"].lower() == stop["Stop_Name"].lower() for s in stops_data):
        return jsonify({"ok": False, "code_http": 400}), 400
    
    # Agregar la nueva parada
    stops_data.append(stop)
    return jsonify({"ok": True, "code_http": 200, "body": stop})

# Endpoint para actualizar una parada
@app.route("/stops/<stop_name>", methods=["PUT"])
def update_stop(stop_name):
    stop = request.get_json()
    # Buscar la parada a actualizar
    existing_stop = next((s for s in stops_data if s["Stop_Name"].lower() == stop_name.lower()), None)
    if not existing_stop:
        return jsonify({"ok": False, "code_http": 404}), 404
    
    # Actualizar la parada
    existing_stop.update(stop)
    return jsonify({"ok": True, "code_http": 200, "body": existing_stop})

# Endpoint para eliminar una parada
@app.route("/stops/<stop_name>", methods=["DELETE"])
def delete_stop(stop_name):
    # Buscar la parada a eliminar
    stop_to_delete = next((s for s in stops_data if s["Stop_Name"].lower() == stop_name.lower()), None)
    if not stop_to_delete:
        return jsonify({"ok": False, "code_http": 404}), 404
    
    # Eliminar la parada
    stops_data.remove(stop_to_delete)
    return jsonify({"ok": True, "code_http": 200, "body": stop_to_delete})

# Endpoint para encontrar la parada más cercana
@app.route("/stops/closest", methods=["GET"])
def get_closest_stop():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    
    closest_stop = None
    min_distance = float('inf')

    for stop in stops_data:
        dist = calculate_distance(latitude, longitude, stop['Latitude'], stop['Longitude'])
        if dist < min_distance:
            closest_stop = stop
            min_distance = dist

    if not closest_stop:
        return jsonify({"ok": False, "code_http": 404}), 404
    
    return jsonify({"ok": True, "code_http": 200, "body": closest_stop})

# Iniciar el servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
