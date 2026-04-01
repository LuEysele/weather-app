# Weather App

## Descripción del proyecto

**Weather App** es una aplicación sencilla desarrollada en Python que permite obtener información meteorológica a partir del nombre de una ciudad. Utiliza la API de Open-Meteo para consultar datos reales del clima y también incluye un módulo de generación de pronósticos sintéticos para pruebas y desarrollo sin conexión.

El proyecto está diseñado con una arquitectura modular para facilitar el aprendizaje de buenas prácticas en desarrollo de software, incluyendo separación de responsabilidades, manejo de errores y pruebas.

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd weather-app
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Guía de uso

Ejecuta la aplicación desde la raíz del proyecto:

```bash
python -m main
```

Ingresa el nombre de una ciudad cuando se solicite.

---

## Ejemplo de salida

```
 Clima en Mérida:

2026-03-31 22:00 — 17.4°C — Fog
2026-03-31 23:00 — 17.8°C — Thunderstorm
2026-04-01 00:00 — 19.6°C — Clear
2026-04-01 01:00 — 20.5°C — Light rain
2026-04-01 02:00 — 20.9°C — Partly cloudy
```

---

## Funcionalidades

* Búsqueda de clima por nombre de ciudad
* Integración con API de Open-Meteo (geocoding + weather)
* Generación de pronóstico sintético reproducible
* Manejo de errores:

  * Ciudad no encontrada
  * Problemas de conexión
  * Respuestas inválidas de API
* Arquitectura modular:

  * `api/` → comunicación con APIs
  * `services/` → lógica del negocio
  * `utils/` → formateo de datos
* Salida formateada amigable para consola

---

## Tecnologías utilizadas

* Python 3.x
* Requests
* Open-Meteo API
* Pytest (para pruebas)

---

## Mejoras futuras

* Interfaz web con Flask o FastAPI
* Interfaz gráfica (GUI)
* Almacenamiento de historial de consultas
* Visualización de datos (gráficas)
* Sistema de caché para reducir llamadas a la API
* Pronóstico extendido (días)
* Soporte multilenguaje
* Pruebas automatizadas más avanzadas (mocking de APIs)
* Modo offline usando datos sintéticos como fallback automático

---

## Autor

Proyecto desarrollado como parte de aprendizaje en herramientas de IA e integración de APIs.

---


## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## Dependencias y Licencias de Terceros

Este proyecto utiliza las siguientes bibliotecas de terceros:

- requests — Licencia MIT  
- pytest — Licencia MIT  
- python-dotenv — Licencia BSD  

Cada biblioteca mantiene su propia licencia y condiciones de uso.