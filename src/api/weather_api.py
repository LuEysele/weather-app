import requests
from src.services.cache_service import get_cached_coords, set_cached_coords

def obtener_clima_actual(ciudad):
    try:
        # -------------------------
        # 1. Geocoding
        # -------------------------
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": ciudad,
            "count": 1
        }

        geo_res = requests.get(geo_url, params=geo_params, timeout=5)

        if not geo_res.ok:
            raise Exception("Error en geocoding")

        geo_data = geo_res.json()

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            raise ValueError("Ciudad no encontrada")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        nombre = geo_data["results"][0]["name"]

        # -------------------------
        # 2. Clima optimizado
        # -------------------------
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,

            # SOLO lo necesario
            "current": "temperature_2m,windspeed_10m,weathercode",

            # mejora de UX
            "timezone": "auto",

            # control de unidades
            "temperature_unit": "celsius"
        }

        weather_res = requests.get(weather_url, params=weather_params, timeout=5)

        if not weather_res.ok:
            raise Exception("Error en API clima")

        weather_data = weather_res.json()

        current = weather_data["current"]

        return {
            "city": nombre,
            "temperature": current["temperature_2m"],
            "windspeed": current["windspeed_10m"],
            "weathercode": current["weathercode"],
            "time": current["time"]
        }

    except requests.exceptions.Timeout:
        return {"error": "Timeout en la solicitud"}
    except requests.exceptions.ConnectionError:
        return {"error": "Error de conexión"}
    except Exception as e:
        return {"error": str(e)}
    
def obtener_pronostico(ciudad):
    # similar a obtener_clima_actual pero con parámetros para pronóstico
    try:
        # -------------------------
        # 1. Geocoding
        # -------------------------
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": ciudad,
            "count": 1
        }

        geo_res = requests.get(geo_url, params=geo_params, timeout=5)

        if not geo_res.ok:
            raise Exception("Error en geocoding")

        geo_data = geo_res.json()

        if "results" not in geo_data or len(geo_data["results"]) == 0:
            raise ValueError("Ciudad no encontrada")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        nombre = geo_data["results"][0]["name"]

        # -------------------------
        # 2. Pronóstico REAL
        # -------------------------
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,

            # predicción horaria
            "hourly": "temperature_2m,weathercode",

            # cuántos días (ajustable)
            "forecast_days": 1,

            # zona horaria
            "timezone": "auto"
        }

        weather_res = requests.get(weather_url, params=weather_params, timeout=5)

        if not weather_res.ok:
            raise Exception("Error en API clima")

        data = weather_res.json()

        # -------------------------
        # 3. Formatear salida
        # -------------------------
        tiempos = data["hourly"]["time"]
        temperaturas = data["hourly"]["temperature_2m"]
        codigos = data["hourly"]["weathercode"]

        items = []

        for i in range(len(tiempos)):
            items.append({
                "time": tiempos[i],
                "temp": temperaturas[i],
                "code": codigos[i]
            })

        return {
            "city": nombre,
            "items": items
        }

    except Exception as e:
        return {"error": str(e)}    

def traducir_clima(code):
    descripciones = {
        0: "Despejado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        61: "Lluvia ligera",
        63: "Lluvia moderada",
        65: "Lluvia fuerte",
        95: "Tormenta"
    }
    return descripciones.get(code, "Desconocido")

def formatear_pronostico(data):
    if "error" in data:
        return f" Error: {data['error']}"

    lineas = [f"\n Pronóstico en {data['city']}:\n"]

    for item in data["items"][:10]:  # solo primeras horas
        linea = f"{item['time']} — {item['temp']}°C — {traducir_clima(item['code'])}"
        lineas.append(linea)

    return "\n".join(lineas)
def obtener_coordenadas(ciudad):
    cached = get_cached_coords(ciudad)

    if cached:
        return cached

    # llamada a API
    lat, lon = ...

    set_cached_coords(ciudad, lat, lon)

    return lat, lon