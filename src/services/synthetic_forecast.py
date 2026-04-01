"""
Módulo para generar previsiones horarias sintéticas reproducibles.

Este módulo simula datos de clima sin usar una API real.
Es útil para pruebas, desarrollo y fallback cuando falla la API.

Salida:
{
    'city': str,
    'units': 'C'|'F',
    'items': [
        {'time_utc': str, 'temp': float, 'description': str},
        ...
    ]
}
"""

from __future__ import annotations

import datetime
import hashlib
import math
import random
from typing import Dict, List


# ----------------------------------------
# Generar seed reproducible por ciudad
# ----------------------------------------
def _seed_from_city(city_name: str) -> int:
    """
    Genera un número entero (seed) a partir del nombre de la ciudad.
    Esto permite que siempre obtengas los mismos datos para la misma ciudad.
    """
    h = hashlib.sha256(city_name.encode("utf-8")).hexdigest()
    return int(h, 16) % (2 ** 32)


# ----------------------------------------
# Conversión de temperatura
# ----------------------------------------
def _c_to_f(c: float) -> float:
    """Convierte grados Celsius a Fahrenheit."""
    return c * 9.0 / 5.0 + 32.0


# ----------------------------------------
# Descripción del clima
# ----------------------------------------
def _generar_descripcion(rnd: random.Random, index: int, seed: int) -> str:
    """
    Genera una descripción de clima pseudo-realista.
    """
    descriptions = [
        "Clear",
        "Few clouds",
        "Partly cloudy",
        "Cloudy",
        "Light rain",
        "Heavy rain",
        "Fog",
        "Thunderstorm",
    ]

    # 10% probabilidad de evento aleatorio
    if rnd.random() < 0.1:
        return rnd.choice(descriptions)

    return descriptions[(index + seed) % len(descriptions)]


# ----------------------------------------
# FUNCIÓN PRINCIPAL
# ----------------------------------------
def generate_synthetic_hourly_forecast(
    city_name: str,
    hours: int = 12,
    units: str = "C"
) -> Dict:
    """
    Genera una previsión horaria sintética.

    Args:
        city_name: Nombre de la ciudad
        hours: Número de horas a simular
        units: 'C' o 'F'

    Returns:
        Diccionario con forecast simulado
    """

    # -------- Validaciones --------
    if not city_name or city_name.strip() == "":
        raise ValueError("El nombre de la ciudad no puede estar vacío.")

    if hours <= 0:
        raise ValueError("hours debe ser mayor que 0.")

    if units not in ("C", "F"):
        raise ValueError("units debe ser 'C' o 'F'.")

    # -------- Configuración inicial --------
    seed = _seed_from_city(city_name)
    rnd = random.Random(seed)

    # Temperatura base dependiente de la ciudad
    base_temp_c = rnd.uniform(10.0, 30.0)

    # Hora actual en UTC (forma moderna)
    start_time = datetime.datetime.now(datetime.timezone.utc).replace(
        minute=0, second=0, microsecond=0
    )

    items: List[Dict] = []

    # -------- Generación de datos --------
    for i in range(hours):
        current_time = start_time + datetime.timedelta(hours=i)

        # Variación diaria tipo seno (simula día/noche)
        variacion = 5.0 * math.sin((i / 3.0))
        ruido = rnd.uniform(-1.5, 1.5)

        temp_c = base_temp_c + variacion + ruido

        # Conversión de unidades
        temp = round(temp_c, 1)
        if units == "F":
            temp = round(_c_to_f(temp_c), 1)

        # Generar descripción
        descripcion = _generar_descripcion(rnd, i, seed)

        # Agregar al resultado
        items.append({
            # Puedes cambiar formato aquí si quieres
            "time_utc": current_time.strftime("%Y-%m-%d %H:%M"),
            "temp": temp,
            "description": descripcion,
        })

    # -------- Resultado final --------
    return {
        "city": city_name,
        "units": units,
        "items": items,
    }
    

forecast = generate_synthetic_hourly_forecast("Mérida", hours=5)

for item in forecast["items"]:
    print(item)