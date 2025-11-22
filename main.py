from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import math
import heapq
from collections import defaultdict

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

# Cargar datos iniciales
try:
    stops_data = load_data()
except Exception as e:
    print(f"Error al cargar los datos: {e}")
    stops_data = []

# Crear la app Flask
app = Flask(__name__)
CORS(app)  # <<<<<< ENABLE CORS PARA WEB Y FLUTTER WEB

# ---------------------------------------------------
#   FUNCIÓN DISTANCIA
# ---------------------------------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ---------------------------------------------------
#   MAPAS AUXILIARES
# ---------------------------------------------------
stops_by_id = {s["id"]: s for s in stops_data}

route_to_stops = defaultdict(set)
stop_to_routes = defaultdict(set)

for stop in stops_data:
    for r in stop.get("routes", []):
        route_to_stops[r].add(stop["id"])
        stop_to_routes[stop["id"]].add(r)


# ---------------------------------------------------
#   PARADA MÁS CERCANA
# ---------------------------------------------------
def closest_stop(latitude, longitude):
    closest = None
    min_distance = float("inf")

    for stop in stops_data:
        d = calculate_distance(latitude, longitude, stop['latitude'], stop['longitude'])
        if d < min_distance:
            min_distance = d
            closest = stop

    return closest, min_distance


# ---------------------------------------------------
#   RECONSTRUIR PATH PARA A*
# ---------------------------------------------------
def reconstruct_path(came_from, goal_state):
    path = []
    current = goal_state

    while current in came_from:
        path.append(current)
        current = came_from[current]

    path.append(current)
    path.reverse()
    return path


# ---------------------------------------------------
#   A* MINIMIZANDO CAMBIOS DE CAMIÓN
# ---------------------------------------------------
def astar_route(start_id, end_id):

    if start_id == end_id:
        return []

    if start_id not in stop_to_routes or end_id not in stops_by_id:
        return None

    BUS_CHANGE_PENALTY = 100.0
    end_stop = stops_by_id[end_id]

    def heuristic(stop_id):
        s = stops_by_id[stop_id]
        return calculate_distance(
            s["latitude"], s["longitude"],
            end_stop["latitude"], end_stop["longitude"]
        )

    open_heap = []
    g_score = {}
    came_from = {}

    start_routes = stop_to_routes.get(start_id, set())
    if not start_routes:
        return None

    for route in start_routes:
        state = (start_id, route)
        g_score[state] = 0.0
        heapq.heappush(open_heap, (heuristic(start_id), state))

    while open_heap:
        f, (current_id, current_bus) = heapq.heappop(open_heap)
        current_state = (current_id, current_bus)

        current_g = g_score.get(current_state, float("inf"))
        if current_g + heuristic(current_id) < f - 1e-9:
            continue

        if current_id == end_id:
            return reconstruct_path(came_from, current_state)

        for route in stop_to_routes[current_id]:
            for neighbor_id in route_to_stops[route]:
                if neighbor_id == current_id:
                    continue

                neighbor_bus = route
                neighbor_state = (neighbor_id, neighbor_bus)

                step_dist = calculate_distance(
                    stops_by_id[current_id]["latitude"],
                    stops_by_id[current_id]["longitude"],
                    stops_by_id[neighbor_id]["latitude"],
                    stops_by_id[neighbor_id]["longitude"],
                )

                change_penalty = 0 if neighbor_bus == current_bus else BUS_CHANGE_PENALTY
                tentative_g = current_g + step_dist + change_penalty

                if tentative_g < g_score.get(neighbor_state, float("inf")):
                    g_score[neighbor_state] = tentative_g
                    came_from[neighbor_state] = current_state
                    heapq.heappush(open_heap, (tentative_g + heuristic(neighbor_id), neighbor_state))

    return None


# ---------------------------------------------------
#   INSTRUCCIONES (TRAMOS)
# ---------------------------------------------------
def build_instructions_from_states(path_states):
    if not path_states:
        return []

    instructions = []
    current_bus = path_states[0][1]
    segment_start_stop_id = path_states[0][0]
    last_stop_id = path_states[0][0]

    for stop_id, bus in path_states[1:]:
        if bus != current_bus:
            instructions.append({
                "from_stop": stops_by_id[segment_start_stop_id],
                "to_stop": stops_by_id[last_stop_id],
                "bus": current_bus
            })
            current_bus = bus
            segment_start_stop_id = last_stop_id

        last_stop_id = stop_id

    instructions.append({
        "from_stop": stops_by_id[segment_start_stop_id],
        "to_stop": stops_by_id[last_stop_id],
        "bus": current_bus
    })

    return instructions


# ---------------------------------------------------
#   ENDPOINTS
# ---------------------------------------------------

@app.route("/paradas")
def get_paradas():
    return jsonify({"ok": True, "body": stops_data})


@app.route("/paradas/<int:id>")
def get_parada(id):
    stop = next((s for s in stops_data if s["id"] == id), None)
    if not stop:
        return jsonify({"ok": False, "message": "Parada no encontrada"}), 404
    return jsonify({"ok": True, "body": stop})


@app.route("/paradas/bus/<name>")
def get_paradas_by_bus(name):
    paradas = [s for s in stops_data if any(name.lower() in r.lower() for r in s["routes"])]
    if not paradas:
        return jsonify({"ok": False, "message": "No se encontraron paradas para este bus"}), 404
    return jsonify({"ok": True, "body": paradas})


@app.route("/paradas/cercana")
def get_parada_cercana():
    try:
        latitude = float(request.args.get("latitude"))
        longitude = float(request.args.get("longitude"))
    except:
        return jsonify({"ok": False, "message": "Parámetros inválidos"}), 400

    stop, distance = closest_stop(latitude, longitude)
    if not stop:
        return jsonify({"ok": False, "message": "No se encontró parada"}), 404

    return jsonify({"ok": True, "body": stop, "distance_km": round(distance, 2)})


@app.route("/instrucciones")
def instrucciones():
    inicio_str = request.args.get("inicio")
    destino_str = request.args.get("destino")

    if not inicio_str or not destino_str:
        return jsonify({"ok": False, "message": "Parámetros requeridos"}), 400

    try:
        i_lat, i_lon = map(float, inicio_str.split(","))
        d_lat, d_lon = map(float, destino_str.split(","))
    except:
        return jsonify({"ok": False, "message": "Formato inválido"}), 400

    start_stop, dist_start = closest_stop(i_lat, i_lon)
    end_stop, dist_end = closest_stop(d_lat, d_lon)

    if not start_stop or not end_stop:
        return jsonify({"ok": False, "message": "No se encontraron paradas"}), 404

    path_states = astar_route(start_stop["id"], end_stop["id"])

    if path_states is None:
        return jsonify({"ok": False, "message": "No hay ruta posible"}), 404

    instructions = build_instructions_from_states(path_states)

    return jsonify({
        "ok": True,
        "start_stop": start_stop,
        "end_stop": end_stop,
        "instructions": instructions,
        "num_buses": len(instructions),
        "start_distance_km": round(dist_start, 3),
        "end_distance_km": round(dist_end, 3)
    })


# Página principal
@app.route("/")
def index():
    año = datetime.now().year
    return render_template("index.html", year=año)


if __name__ == "__main__":
    app.run(debug=True)
