# Ko'ox API

## Página Interactiva

La **Ko'ox API** es una API pública de código abierto que se encuentra disponible para su uso a través de una interfaz web interactiva. Puedes acceder a la documentación de la API y explorar sus endpoints desde el siguiente enlace:

**[Ko'ox API - Documentación interactiva](https://koox-api.vercel.app/)**

## Descripción

**Ko'ox API** es un proyecto de código abierto diseñado para gestionar y consultar las paradas del sistema de transporte público Ko'ox en Campeche. Esta API RESTful permite a los usuarios acceder a la información de las paradas, obtener la más cercana a una ubicación geográfica específica, y filtrar paradas por rutas de autobús.

El propósito principal de este proyecto es aportar a la comunidad de Campeche proporcionando una herramienta útil para mejorar la movilidad urbana, permitiendo a los ciudadanos acceder fácilmente a la información sobre las paradas del sistema Ko'ox. La API fue desarrollada por **Jose Manuel Castillo Queh**, de 20 años, como parte de un proyecto de programación avanzada para la **Universidad Autónoma de Campeche**.

## Contexto y Origen del Proyecto

Este proyecto nació como una propuesta para contribuir al bienestar y desarrollo de la comunidad de Campeche. Como usuario habitual del transporte público, me di cuenta de la problemática relacionada con las paradas de Ko'ox, así como la dispersión y falta de accesibilidad de la información en internet. 

Fue entonces cuando decidí, **Jose Manuel Castillo Queh**, de 20 años, emprender el desarrollo de una solución que pudiera ser aprovechada por la comunidad: una API que centralice la información sobre las paradas de Ko'ox. Este trabajo es el resultado de un esfuerzo de investigación, durante el cual logré recopilar datos dispersos y no expuestos de diversas fuentes disponibles en internet. La tarea no fue fácil, pero con dedicación y esfuerzo, creé una base de datos que sirve de apoyo para esta solución.

El propósito principal de la **Ko'ox API** es empoderar a la sociedad campechana, proporcionando un recurso accesible y confiable para consultar la información sobre las paradas y rutas del transporte público. Esta API busca que cualquier persona pueda beneficiarse de ella para facilitar su vida diaria al momento de usar el servicio de Ko'ox.

Además, en el futuro cercano, estamos trabajando en el desarrollo de una aplicación móvil basada en esta API, que se podrá descargar de manera gratuita como un archivo APK, sin ningún riesgo ni costo. Esta aplicación permitirá a los usuarios acceder a la información de manera más cómoda y sencilla desde sus teléfonos, mejorando aún más la experiencia del usuario.

Este proyecto tiene un fuerte componente social, ya que la finalidad es mejorar la calidad de vida de los habitantes de Campeche, fomentar el uso del transporte público y mantenerlos informados sobre las actualizaciones impulsadas por el gobierno de **Layda Sansores San Román**, presidenta de Campeche.

## Requisitos

- **Python 3.7+**
- **Flask** (usado para desarrollar la API)
- **Dependencias necesarias** (todas las dependencias necesarias están listadas en el archivo `requirements.txt`)

## Instalación y Ejecución Local

Para ejecutar **Ko'ox API** localmente en tu máquina, sigue estos pasos:

### 1. Clonar el repositorio

Primero, clona el repositorio en tu máquina:

```bash
git clone https://github.com/CastilloDevX/koox_api.git
````

### 2. Crear un entorno virtual

Es recomendable crear un entorno virtual para manejar las dependencias del proyecto:

* En Windows:

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

* En Linux/macOS:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar dependencias

Una vez activado el entorno virtual, instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la API

Ahora, ejecuta el servidor localmente:

```bash
python app.py
```

El servidor se ejecutará en `http://localhost:5000`.

### 5. Acceso a la API

Una vez que la API esté corriendo, puedes acceder a los diferentes endpoints. Por ejemplo:

* Obtener todas las paradas: `GET http://localhost:5000/paradas`
* Obtener una parada por ID: `GET http://localhost:5000/paradas/9`
* Obtener la parada más cercana: `GET http://localhost:5000/paradas/cercana?latitude=18.6470&longitude=-91.8240`
* Y mucho más, según lo descrito en la sección de **Endpoints**.

## Endpoints

### 1. Obtener todas las paradas

**GET** `/paradas`

* Devuelve la lista completa de las paradas.

**Ejemplo de respuesta:**

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
    },
    ...
  ]
}
```

### 2. Obtener una parada específica por ID

**GET** `/paradas/<id>`

* Devuelve los detalles de una parada específica.

**Ejemplo de respuesta:**

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

### 3. Obtener paradas por ruta de bus

**GET** `/paradas/bus/<name>`

* Devuelve las paradas que contienen una ruta específica.

**Ejemplo de respuesta:**

```json
{
  "ok": true,
  "code_http": 200,
  "body": [
    {
      "id": 1,
      "stop_name": "Calle 105-A",
      "latitude": 19.842192,
      "longitude": -90.508463,
      "routes": [
        "Koox 01 Troncal Eje Principal",
        "Koox 06 Amp. Bellavista - Revolución Circ. 1",
        "Koox 08 Carmelo-Esperanza"
      ]
    },
    ...
  ],
  "total": 15
}
```

### 4. Encontrar la parada más cercana

**GET** `/paradas/cercana`

* Encuentra la parada más cercana a una ubicación.

**Ejemplo de respuesta:**

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
  },
  "distance_km": 1.5
}
```

### 5. Encontrar la parada más cercana para una ruta específica

**GET** `/paradas/cercana/ruta`

* Encuentra la parada más cercana que tenga una ruta específica.

**Ejemplo de respuesta:**

```json
{
  "ok": true,
  "code_http": 200,
  "body": {
    "id": 22,
    "stop_name": "Pedro Moreno",
    "latitude": 19.838979,
    "longitude": -90.538881,
    "routes": [
      "Koox 01 Troncal Eje Principal",
      "Koox 28 Troncal Eje Oriente",
      "Koox 29 Troncal Eje Norte"
    ]
  },
  "distance_km": 189.13,
  "num_stops_with_route": 59
}
```

## Notas Importantes

* La API ahora permite encontrar la parada más cercana tanto con o sin especificar una ruta.
* La API busca paradas por nombre sin distinguir mayúsculas y minúsculas.
* Los datos se almacenan en memoria durante la ejecución del servidor, y no se persisten en el archivo JSON original.
* La distancia se calcula en kilómetros usando la fórmula de Haversine.

## Licencia

Este proyecto está bajo la **Licencia MIT**.