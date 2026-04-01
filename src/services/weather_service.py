# src/services/weather_service.py
from src.api.weather_api import obtener_clima_actual, obtener_pronostico
#from src.services.synthetic_forecast import generate_synthetic_hourly_forecast

def obtener_clima_completo(ciudad):
    try:
        actual = obtener_clima_actual(ciudad)
        pronostico = obtener_pronostico(ciudad)

        if "error" in actual and "error" in pronostico:
            return {"error": "No se pudo obtener información"}

        return {
            "actual": actual,
            "forecast": pronostico
        }

    except Exception as e:
        return {"error": str(e)}


