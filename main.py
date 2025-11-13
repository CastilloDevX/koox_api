from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import math

# Archivo JSON
JSON_FILE = 'db/koox_stops_routes.json'

# Función para cargar datos
def load_data():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"El archivo {JSON_FILE} no fue encontrado.")
    except json.JSONDecodeError:
        raise Exception(f"Error al decodificar el archivo JSON.")
        
# Cargar los datos iniciales
try:
    stops_data = load_data()
except Exception as e:
    print(f"Error al cargar los datos: {e}")
    stops_data = []

# Crear la app Flask
app = Flask(__name__)

# Función para calcular la distancia entre dos puntos geográficos (en km)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Obtener todas las paradas (sin paginación)
@app.route("/paradas", methods=["GET"])
def get_paradas():
    return jsonify({"ok": True, "code_http": 200, "body": stops_data})

# Obtener una parada por ID
@app.route("/paradas/<int:id>", methods=["GET"])
def get_parada(id):
    stop = next((s for s in stops_data if s["id"] == id), None)
    if not stop:
        return jsonify({"ok": False, "code_http": 404, "message": "Parada no encontrada"}), 404
    return jsonify({"ok": True, "code_http": 200, "body": stop})

# Obtener paradas por ruta de bus
@app.route("/paradas/bus/<name>", methods=["GET"])
def get_paradas_by_bus(name):
    # Buscar paradas que contengan la ruta especificada
    paradas_encontradas = []
    
    for stop in stops_data:
        # Buscar si alguna ruta contiene el nombre del bus (case insensitive)
        for route in stop.get("routes", []):
            if name.lower() in route.lower():
                paradas_encontradas.append(stop)
                break  # Evitar duplicados si hay múltiples coincidencias
    
    if not paradas_encontradas:
        return jsonify({
            "ok": False, 
            "code_http": 404, 
            "message": f"No se encontraron paradas para el bus '{name}'"
        }), 404
    
    return jsonify({
        "ok": True, 
        "code_http": 200, 
        "body": paradas_encontradas,
        "total": len(paradas_encontradas)
    })

# Obtener la parada más cercana
@app.route("/paradas/cercana", methods=["GET"])
def get_parada_cercana():
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({
            "ok": False, 
            "code_http": 400, 
            "message": "Se requieren parámetros 'latitude' y 'longitude' válidos"
        }), 400
    
    closest_stop = None
    min_distance = float('inf')

    for stop in stops_data:
        dist = calculate_distance(latitude, longitude, stop['latitude'], stop['longitude'])
        if dist < min_distance:
            closest_stop = stop
            min_distance = dist

    if not closest_stop:
        return jsonify({"ok": False, "code_http": 404, "message": "No se encontró parada cercana"}), 404
    
    return jsonify({
        "ok": True, 
        "code_http": 200, 
        "body": closest_stop, 
        "distance_km": round(min_distance, 2)
    })

# Obtener la parada más cercana para una ruta específica
@app.route("/paradas/cercana/ruta", methods=["GET"])
def get_parada_cercana_por_ruta():
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        ruta = request.args.get('ruta')
        
        if not ruta:
            return jsonify({
                "ok": False, 
                "code_http": 400, 
                "message": "Se requiere el parámetro 'ruta'"
            }), 400
            
    except (TypeError, ValueError):
        return jsonify({
            "ok": False, 
            "code_http": 400, 
            "message": "Se requieren parámetros 'latitude', 'longitude' y 'ruta' válidos"
        }), 400
    
    # Filtrar paradas que contengan la ruta especificada
    paradas_con_ruta = []
    
    for stop in stops_data:
        for route in stop.get("routes", []):
            if ruta.lower() in route.lower():
                paradas_con_ruta.append(stop)
                break
    
    if not paradas_con_ruta:
        return jsonify({
            "ok": False, 
            "code_http": 404, 
            "message": f"No se encontraron paradas con la ruta '{ruta}'"
        }), 404
    
    # Encontrar la parada más cercana entre las que tienen la ruta
    closest_stop = None
    min_distance = float('inf')
    
    for stop in paradas_con_ruta:
        dist = calculate_distance(latitude, longitude, stop['latitude'], stop['longitude'])
        if dist < min_distance:
            closest_stop = stop
            min_distance = dist
    
    if not closest_stop:
        return jsonify({
            "ok": False, 
            "code_http": 404, 
            "message": "No se encontró parada cercana con esa ruta"
        }), 404
    
    return jsonify({
        "ok": True, 
        "code_http": 200, 
        "body": closest_stop, 
        "distance_km": round(min_distance, 2),
        "search_route": ruta,
        "num_stops_with_route": len(paradas_con_ruta)
    })

# Página principal (index)
@app.route('/')
def index():
    current_year = datetime.now().year
    return render_template('index.html', year=current_year)

if __name__ == "__main__":
    app.run(debug=True)