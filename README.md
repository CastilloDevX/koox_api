# Koox Stops Routes API

API REST desarrollada con Flask para gestionar paradas de transporte público y encontrar la parada más cercana a una ubicación específica.

## Requisitos

- Python 3.7+
- Flask

## Instalación

1. Clona el repositorio o descarga los archivos

2. Instala las dependencias:
```bash
pip install flask
```

3. Asegúrate de tener el archivo de datos en la ruta correcta:
```
db/koox_stops_routes.json
```

4. Inicia el servidor:
```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

## Estructura de Datos

Cada parada debe tener la siguiente estructura:

```json
{
  "Stop_Name": "Nombre de la Parada",
  "Latitude": 18.6465,
  "Longitude": -91.8235,
  "Routes": ["Ruta 1", "Ruta 2"]
}
```

## Endpoints

### 1. Obtener todas las paradas

**GET** `/stops`

Retorna la lista completa de paradas.

**Respuesta exitosa:**
```json
{
  "ok": true,
  "code_http": 200,
  "body": [
    {
      "Stop_Name": "Parada Central",
      "Latitude": 18.6465,
      "Longitude": -91.8235,
      "Routes": ["Ruta 1", "Ruta 2"]
    }
  ]
}
```

**Ejemplo con curl:**
```bash
curl http://localhost:5000/stops
```

---

### 2. Obtener una parada específica

**GET** `/stops/<stop_name>`

Retorna los detalles de una parada específica por nombre.

**Parámetros:**
- `stop_name` (string): Nombre de la parada (no sensible a mayúsculas/minúsculas)

**Respuesta exitosa:**
```json
{
  "ok": true,
  "code_http": 200,
  "body": {
    "Stop_Name": "Parada Central",
    "Latitude": 18.6465,
    "Longitude": -91.8235,
    "Routes": ["Ruta 1"]
  }
}
```

**Respuesta de error (404):**
```json
{
  "ok": false,
  "code_http": 404
}
```

**Ejemplo con curl:**
```bash
curl http://localhost:5000/stops/Parada%20Central
```

---

### 3. Crear una nueva parada

**POST** `/stops`

Crea una nueva parada en el sistema.

**Body (JSON):**
```json
{
  "Stop_Name": "Nueva Parada",
  "Latitude": 18.6500,
  "Longitude": -91.8300,
  "Routes": ["Ruta 3"]
}
```

**Respuesta exitosa:**
```json
{
  "ok": true,
  "code_http": 200,
  "body": {
    "Stop_Name": "Nueva Parada",
    "Latitude": 18.6500,
    "Longitude": -91.8300,
    "Routes": ["Ruta 3"]
  }
}
```

**Respuesta de error (400):**
```json
{
  "ok": false,
  "code_http": 400
}
```
*La parada ya existe en el sistema*

**Ejemplo con curl:**
```bash
curl -X POST http://localhost:5000/stops \
  -H "Content-Type: application/json" \
  -d '{
    "Stop_Name": "Nueva Parada",
    "Latitude": 18.6500,
    "Longitude": -91.8300,
    "Routes": ["Ruta 3"]
  }'
```

---

### 4. Actualizar una parada

**PUT** `/stops/<stop_name>`

Actualiza la información de una parada existente.

**Parámetros:**
- `stop_name` (string): Nombre de la parada a actualizar

**Body (JSON):**
```json
{
  "Latitude": 18.6550,
  "Longitude": -91.8350,
  "Routes": ["Ruta 1", "Ruta 4"]
}
```

**Respuesta exitosa:**
```json
{
  "ok": true,
  "code_http": 200,
  "body": {
    "Stop_Name": "Parada Central",
    "Latitude": 18.6550,
    "Longitude": -91.8350,
    "Routes": ["Ruta 1", "Ruta 4"]
  }
}
```

**Respuesta de error (404):**
```json
{
  "ok": false,
  "code_http": 404
}
```

**Ejemplo con curl:**
```bash
curl -X PUT http://localhost:5000/stops/Parada%20Central \
  -H "Content-Type: application/json" \
  -d '{
    "Latitude": 18.6550,
    "Longitude": -91.8350,
    "Routes": ["Ruta 1", "Ruta 4"]
  }'
```

---

### 5. Eliminar una parada

**DELETE** `/stops/<stop_name>`

Elimina una parada del sistema.

**Parámetros:**
- `stop_name` (string): Nombre de la parada a eliminar

**Respuesta exitosa:**
```json
{
  "ok": true,
  "code_http": 200,
  "body": {
    "Stop_Name": "Parada Central",
    "Latitude": 18.6465,
    "Longitude": -91.8235,
    "Routes": ["Ruta 1"]
  }
}
```

**Respuesta de error (404):**
```json
{
  "ok": false,
  "code_http": 404
}
```

**Ejemplo con curl:**
```bash
curl -X DELETE http://localhost:5000/stops/Parada%20Central
```

---

### 6. Encontrar la parada más cercana

**GET** `/stops/closest`

Encuentra la parada más cercana a una ubicación geográfica específica utilizando el cálculo de distancia Haversine.

**Query Parameters:**
- `latitude` (float): Latitud de la ubicación
- `longitude` (float): Longitud de la ubicación

**Respuesta exitosa:**
```json
{
  "ok": true,
  "code_http": 200,
  "body": {
    "Stop_Name": "Parada Central",
    "Latitude": 18.6465,
    "Longitude": -91.8235,
    "Routes": ["Ruta 1", "Ruta 2"]
  }
}
```

**Respuesta de error (404):**
```json
{
  "ok": false,
  "code_http": 404
}
```

**Ejemplo con curl:**
```bash
curl "http://localhost:5000/stops/closest?latitude=18.6470&longitude=-91.8240"
```

## Notas Importantes

- La API busca paradas por nombre sin distinguir mayúsculas y minúsculas
- Los datos se almacenan en memoria durante la ejecución del servidor
- Las modificaciones no se persisten en el archivo JSON original
- La distancia se calcula en kilómetros usando la fórmula Haversine
- El servidor corre en modo debug por defecto (desactivar en producción)

## Códigos de Estado HTTP

- `200`: Operación exitosa
- `400`: Solicitud incorrecta (ej: parada duplicada)
- `404`: Recurso no encontrado

## Mejoras Futuras Sugeridas

- Implementar persistencia de datos en el archivo JSON
- Añadir autenticación y autorización
- Implementar paginación para el endpoint de todas las paradas
- Agregar validación de datos de entrada
- Implementar búsqueda por ruta
- Añadir límite de distancia para la búsqueda de paradas cercanas

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.