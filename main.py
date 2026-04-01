# main.py
import sys
sys.stdout.reconfigure(encoding='utf-8')
from src.services.weather_service import obtener_clima_completo
from src.utils.formatter import formatear_clima_completo


def probar_ciudad(ciudad):
    print("\n" + "="*50)
    print(f" Probando ciudad: {ciudad}")
    print("="*50)

    data = obtener_clima_completo(ciudad)
    resultado = formatear_clima_completo(data)

    print(resultado)


def main():
    # Casos de prueba
    ciudades = [
        "Mérida",      # ciudad con acento
        "Tokyo",       # internacional
        "Paris",       # múltiples coincidencias
        "New York",    # nombre compuesto
        "asdfghjkl"    # inválida
    ]

    for ciudad in ciudades:
        probar_ciudad(ciudad)


if __name__ == "__main__":
    main()