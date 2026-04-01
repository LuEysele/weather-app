import requests

def get_weather(city):
    try:
        # 1. Obtener coordenadas
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {
            "name": city,
            "count": 1
        }

        geo_response = requests.get(geo_url, params=geo_params)

        if not geo_response.ok:
            raise Exception("Error en geocoding")

        geo_data = geo_response.json()

        if "results" not in geo_data:
            raise Exception("Ciudad no encontrada")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        # 2. Obtener clima
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }

        weather_response = requests.get(weather_url, params=weather_params)

        if not weather_response.ok:
            raise Exception("Error en API clima")

        return weather_response.json()

    except Exception as e:
        return {"error": str(e)}


print(get_weather("Tokyo"))
print(get_weather("Mérida"))

def test_get_weather():
    ciudades = ["Tokyo", "Mérida", "Paris", ""]

    for ciudad in ciudades:
        resultado = get_weather(ciudad)
        print(f"Test con: {ciudad} → {resultado}")

test_get_weather()