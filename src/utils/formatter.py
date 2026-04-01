# src/utils/formatter.py
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


def formatear_clima_completo(data):
    if "error" in data:
        return f"Error: {data['error']}"

    lineas = []

    # Clima actual
    if data["actual"] and "error" not in data["actual"]:
        actual = data["actual"]
        lineas.append(f"\n Clima actual en {actual['city']}:")
        lineas.append(f"{actual['time']} — {actual['temperature']}°C — {actual['windspeed']} km/h")

    # Pronóstico
    if data["forecast"] and "error" not in data["forecast"]:
        lineas.append("\n Pronóstico:")

        for item in data["forecast"]["items"][:8]:  # primeras horas
            linea = f"{item['time']} — {item['temp']}°C — {traducir_clima(item['code'])}"
            lineas.append(linea)

    return "\n".join(lineas)

def formatear_forecast(forecast):
    """
    Convierte el forecast en texto legible para consola.
    """
    if "error" in forecast:
        return f" Error: {forecast['mensaje']}"

    lineas = [f"\n Clima en {forecast['city']}:\n"]

    for item in forecast["items"]:
        linea = f"{item['time_utc']} — {item['temp']}°{forecast['units']} — {item['description']}"
        lineas.append(linea)

    return "\n".join(lineas)
