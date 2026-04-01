async function obtenerClima(ciudad) {
    try {
        // Validar entrada
        if (!ciudad || ciudad.trim() === "") {
            throw new Error("Debes ingresar un nombre de ciudad válido.");
        }

        // 1. Obtener coordenadas (Geocoding)
        const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(ciudad)}&count=1&language=es&format=json`;
        const geoResponse = await fetch(geoUrl);

        // Verificar respuesta HTTP
        if (!geoResponse.ok) {
            throw new Error("Error al obtener coordenadas de la ciudad.");
        }

        const geoData = await geoResponse.json();

        // Validar si la ciudad existe
        if (!geoData.results || geoData.results.length === 0) {
            throw new Error("Ciudad no encontrada.");
        }

        const { latitude, longitude, name } = geoData.results[0];

        // 2. Obtener clima actual
        const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`;
        const weatherResponse = await fetch(weatherUrl);

        if (!weatherResponse.ok) {
            throw new Error("Error al obtener datos del clima.");
        }

        const weatherData = await weatherResponse.json();

        if (!weatherData.current_weather) {
            throw new Error("No se pudo obtener el clima actual.");
        }

        const temperatura = weatherData.current_weather.temperature;
        const codigoClima = weatherData.current_weather.weathercode;

        // Función simple para describir el clima
        function descripcionClima(code) {
            const descripciones = {
                0: "Despejado",
                1: "Mayormente despejado",
                2: "Parcialmente nublado",
                3: "Nublado",
                45: "Niebla",
                48: "Niebla con escarcha",
                51: "Llovizna ligera",
                61: "Lluvia ligera",
                63: "Lluvia moderada",
                65: "Lluvia fuerte",
                80: "Chubascos",
                95: "Tormenta"
            };
            return descripciones[code] || "Condición desconocida";
        }

        // 3. Retornar resultado en formato JSON
        return {
            ciudad: name,
            temperatura: temperatura,
            descripcion: descripcionClima(codigoClima)
        };

    } catch (error) {
        // Manejo de errores general
        return {
            error: true,
            mensaje: error.message
        };
    }
}

obtenerClima("Mérida")
    .then(resultado => console.log(resultado))
    .catch(error => console.error(error));