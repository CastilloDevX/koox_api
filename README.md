# API Abierta de las paradas KO'OX Campeche

API REST desarrollada con **Flask** para gestionar paradas de transporte público y encontrar la parada más cercana a una ubicación específica.

## Requisitos

- **Python 3.7+**
- **Flask**
- **python-dotenv** (para manejar variables de entorno)

## Instalación

### 1. Clona el repositorio o descarga los archivos
Puedes clonar el repositorio usando el siguiente comando:

```bash
git clone https://github.com/CastilloDevX/koox_api.git
````

### 2. Instala las dependencias

Este proyecto utiliza un entorno virtual (`venv`). Para instalar las dependencias, sigue estos pasos:

1. Activa el entorno virtual:

   * En Windows:

     ```bash
     venv\Scripts\activate
     ```
   * En Linux/macOS:

     ```bash
     source venv/bin/activate
     ```

2. Instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

### 3. Inicia el servidor localmente

Para ejecutar la API en tu máquina local, usa el siguiente comando:

```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`.

### 4. Despliegue en Vercel

Si prefieres acceder a la API desde Vercel, puedes utilizar el siguiente enlace para acceder al servidor desplegado:

[https://koox-api.vercel.app/](https://koox-api.vercel.app/)

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

**GET** `/paradas`

* Retorna la lista completa de paradas.

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
curl https://koox-api.vercel.app/paradas
```

---

### 2. Obtener una parada específica

**GET** `/paradas/<int:id>`

* Retorna los detalles de una parada específica por ID.

**Parámetros:**

* `id` (entero): ID de la parada.

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
curl https://koox-api.vercel.app/paradas/1
```

---

### 3. Obtener paradas por ruta de bus

**GET** `/paradas/bus/<name>`

* Retorna las paradas que están asociadas a una ruta de bus específica.

**Parámetros:**

* `name` (string): Nombre de la ruta de bus (no sensible a mayúsculas/minúsculas).

**Respuesta exitosa:**

```json
{
  "ok": true,
  "code_http": 200,
  "body": [
    {
      "Stop_Name": "Jardines",
      "Latitude": 19.842517,
      "Longitude": -90.535564,
      "Routes": ["Koox 15 Jardines"]
    }
  ],
  "total": 1
}
```

**Ejemplo con curl:**

```bash
curl https://koox-api.vercel.app/paradas/bus/Koox%2015%20Jardines
```

---

### 4. Obtener la parada más cercana

**GET** `/paradas/cercana`

* Encuentra la parada más cercana a una ubicación geográfica específica.

**Parámetros requeridos:**

* `latitude`: Latitud de la ubicación.
* `longitude`: Longitud de la ubicación.

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
  },
  "distance_km": 1.23
}
```

**Ejemplo con curl:**

```bash
curl "https://koox-api.vercel.app/paradas/cercana?latitude=18.6470&longitude=-91.8240"
```

---

### 5. Obtener la parada más cercana para una ruta específica

**GET** `/paradas/cercana/ruta`

* Encuentra la parada más cercana que tenga una ruta específica.

**Parámetros requeridos:**

* `latitude`: Latitud de la ubicación.
* `longitude`: Longitud de la ubicación.
* `ruta`: Nombre de la ruta de bus.

**Ejemplo de solicitud:**

```bash
curl "https://koox-api.vercel.app/paradas/cercana/ruta?latitude=18.6470&longitude=-91.8240&ruta=Koox%2015%20Jardines"
```

**Respuesta de ejemplo:**

```json
{
  "ok": true, 
  "code_http": 200, 
  "body": {
    "Stop_Name": "Jardines",
    "Latitude": 19.842517,
    "Longitude": -90.535564,
    "Routes": ["Koox 15 Jardines"]
  },
  "distance_km": 0.75,
  "search_route": "Koox 15 Jardines",
  "num_stops_with_route": 10
}
```

---

### 6. Página principal (Interfaz web)

**Ruta:** `/`
**Método:** `GET`
**Descripción:** Carga una página de inicio básica que muestra el año actual.
**Ejemplo de solicitud:**

```bash
http://127.0.0.1:5000/
```

---

## Notas Importantes

* La API busca paradas por nombre sin distinguir mayúsculas y minúsculas.
* Los datos se almacenan en memoria durante la ejecución del servidor.
* Las modificaciones no se persisten en el archivo JSON original.
* La distancia se calcula en kilómetros usando la fórmula Haversine.
* El servidor corre en modo **debug** por defecto (desactivar en producción).

## Códigos de Estado HTTP

* `200`: Operación exitosa.
* `400`: Solicitud incorrecta (ej: parámetro faltante o inválido).
* `404`: Recurso no encontrado.

## Mejoras Futuras Sugeridas

* Implementar persistencia de datos en el archivo JSON.
* Añadir autenticación y autorización.
* Implementar paginación para el endpoint de todas las paradas.
* Agregar validación de datos de entrada.
* Implementar búsqueda por ruta.
* Añadir límite de distancia para la búsqueda de paradas cercanas.

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia **MIT**.

### ¿Cómo descargar el archivo?

He preparado el archivo `README.md` para ti. Puedes **descargarlo** haciendo clic en el siguiente enlace:

[Descargar README.md](sandbox:/mnt/data/README.md)

Si tienes alguna otra pregunta o necesitas más ayuda, no dudes en preguntar. ¡Suerte con tu API! 🚀