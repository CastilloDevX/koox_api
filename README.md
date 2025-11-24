# 🚌 Ko'ox API – Transporte Público de Campeche

API pública, open-source y desarrollada con Flask para consultar paradas del sistema de transporte Ko’ox.

## ⚠️ ADVERTENCIA IMPORTANTE

**Esta API NO ES OFICIAL y NO TIENE NINGUNA RELACIÓN con el gobierno de Campeche.**
Es un proyecto experimental, en fase BETA, sujeto a errores, datos imprecisos y cambios constantes.

El creador, **Jose Manuel Castillo Queh**, no se hace responsable de inconvenientes, problemas gubernamentales ni usos indebidos derivados de esta API.
_Úsala bajo tu propio riesgo._

## 🌐 Página Interactiva (Documentación + Tester)

Puedes explorar todos los endpoints en una interfaz web:

👉 https://koox-api.vercel.app/

## 📘 Descripción del Proyecto

La Ko'ox API es una API RESTful diseñada para consultar las paradas del sistema de transporte Ko’ox de la ciudad de Campeche. Su objetivo es proporcionar a la comunidad una herramienta sencilla y accesible que permita:

- Ver todas las paradas del transporte.
- Encontrar la parada más cercana mediante geolocalización.
- Buscar paradas por ruta de autobús.
- Obtener instrucciones de viaje usando A* minimizando cambios de camión (nuevo).

Este proyecto fue desarrollado por Jose Manuel Castillo Queh (20 años) como una contribución social y como parte de un proyecto académico de programación avanzada en la Universidad Autónoma de Campeche.

## 🏛️ Contexto y Origen del Proyecto

El proyecto surge al detectar:

- Falta de información centralizada sobre las paradas Ko’ox.
- Datos dispersos y poco accesibles para los ciudadanos.
- Necesidad de una solución moderna, gratuita y abierta.

Tras investigar múltiples fuentes y recopilar información no publicada de forma accesible, se construyó una base de datos estructurada y una API pública para que cualquier ciudadano pueda consultarla libremente.

Además, se trabaja en una aplicación móvil APK gratuita (sin riesgos y sin costo) basada en esta API, para mejorar aún más la experiencia de uso.

## 🔧 Requisitos

- Python 3.7+
- Flask
- Dependencias listadas en requirements.txt

## 🖥️ Instalación y Ejecución Local

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/CastilloDevX/koox_api.git
cd koox_api
```

### 2️⃣ Crear un entorno virtual

Windows
```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la API
```bash
python app.py
```

Servidor disponible en:

👉 http://localhost:5000

## 🚏 Endpoints Disponibles

A continuación se muestran ejemplos reales obtenidos desde la API desplegada:

### 1. 📍 Obtener todas las paradas
GET /paradas

Ejemplo de respuesta real:
```json
{
  "ok": true,
  "code_http": 200,
  "body": [
    {
      "id": 1,
      "stop_name": "Alameda",
      "latitude": 19.841517,
      "longitude": -90.534564,
      "routes": [
        "Koox 01 Troncal Eje Principal",
        "Koox 27 Troncal Eje Central",
        "Koox 28 Troncal Eje Oriente",
        "Koox 29 Troncal Eje Norte"
      ]
    }
  ]
}
```

### 2. 🔍 Obtener una parada por ID
GET /paradas/<id>

Ejemplo real (/paradas/9):
```json
{
  "ok": true,
  "code_http": 200,
  "body": {
    "id": 9,
    "stop_name": "Calle 105-A",
    "latitude": 19.842192,
    "longitude": -90.508463,
    "routes": [
      "Koox 01 Troncal Eje Principal",
      "Koox 06 Amp. Bellavista - Revolución Circ. 1",
      "Koox 08 Carmelo-Esperanza"
    ]
  }
}
```

### 3. 🚌 Obtener paradas por nombre de ruta
GET /paradas/bus/<name>

Ejemplo real (/paradas/bus/Jardines):
```json
{
  "ok": true,
  "code_http": 200,
  "body": [
    {
      "id": 2,
      "stop_name": "Chihuahua",
      "latitude": 19.843134,
      "longitude": -90.530806,
      "routes": [
        "Koox 01 Troncal Eje Principal",
        "Koox 15 Jardines",
        "Koox 16 Polvorín - Paso de las Águilas",
        "Koox 18 San Francisco",
        "Koox 28 Troncal Eje Oriente",
        "Koox 29 Troncal Eje Norte"
      ]
    }
  ],
  "total": 15
}
```

### 4. 📡 Parada más cercana
GET /paradas/cercana?latitude=X&longitude=Y

Ejemplo real:
```json
{
  "ok": true,
  "body": {
    "id": 437,
    "stop_name": "Hospital",
    "latitude": 19.789902,
    "longitude": -90.619589,
    "routes": [
      "Koox 22 Lerma - Tec",
      "Koox 23 Kila - Marañón"
    ]
  },
  "distance_km": 179.28
}
```

### 5. 🧭 Obtener instrucciones (A*)

Minimiza cambios de camión.

GET _/instrucciones?inicio=lat,lon&destino=lat,lon_

Ejemplo real:
```json
{
  "ok": true,
  "num_buses": 1,
  "start_stop": {
    "id": 2,
    "stop_name": "Chihuahua"
  },
  "end_stop": {
    "id": 9,
    "stop_name": "Calle 105-A"
  },
  "instructions": [
    {
      "bus": "Koox 01 Troncal Eje Principal",
      "from_stop": "Chihuahua",
      "to_stop": "Calle 105-A"
    }
  ]
}
```

## 📝 Notas Importantes

- La API mantiene los datos en memoria mientras el servidor está en ejecución.

- Las búsquedas no distinguen mayúsculas/minúsculas.

- Se utiliza la fórmula Haversine para calcular distancia geográfica.

- Endpoint _/paradas/cercana/ruta_ ya no existe en la versión actual.

- El endpoint _/instrucciones_ implementa A* con penalización por cambio de camión.

## 📄 Licencia

Este proyecto está bajo la licencia MIT.
Puedes usarlo, modificarlo y distribuirlo libremente con atribución.