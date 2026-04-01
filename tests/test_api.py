import types
from main import obtener_temperatura


class FakeResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self):
        return self._json_data


def make_get_responses(responses):
    """Return a function that returns successive FakeResponse objects from the list."""
    calls = {"i": 0}

    def _get(url, *args, **kwargs):
        if calls["i"] >= len(responses):
            # If more calls than expected, return a default 500 response
            return FakeResponse(status_code=500)
        resp = responses[calls["i"]]
        calls["i"] += 1
        return resp

    return _get


def test_geocode_non_200(monkeypatch, capsys):
    # First request (geocoding) returns 500
    monkeypatch.setattr("requests.get", make_get_responses([FakeResponse(status_code=500)]))
    obtener_temperatura("CiudadX")
    captured = capsys.readouterr()
    assert "Error al geocodificar la ciudad." in captured.out


def test_geocode_empty_list(monkeypatch, capsys):
    # Geocoding returns 200 but empty list
    monkeypatch.setattr(
        "requests.get",
        make_get_responses([FakeResponse(status_code=200, json_data=[])]),
    )
    obtener_temperatura("CiudadX")
    captured = capsys.readouterr()
    assert "Ciudad no encontrada." in captured.out


def test_weather_non_200(monkeypatch, capsys):
    # Geocoding succeeds, weather API returns 500
    geo = FakeResponse(status_code=200, json_data=[{"lat": "1.0", "lon": "2.0"}])
    weather_fail = FakeResponse(status_code=500)
    monkeypatch.setattr("requests.get", make_get_responses([geo, weather_fail]))

    obtener_temperatura("CiudadX")
    captured = capsys.readouterr()
    assert "Error al obtener los datos del clima." in captured.out


def test_unexpected_weather_format(monkeypatch, capsys):
    # Geocoding succeeds, weather returns 200 but missing expected keys
    geo = FakeResponse(status_code=200, json_data=[{"lat": "1.0", "lon": "2.0"}])
    bad_weather = FakeResponse(status_code=200, json_data={"no_current": {}})
    monkeypatch.setattr("requests.get", make_get_responses([geo, bad_weather]))

    obtener_temperatura("CiudadX")
    captured = capsys.readouterr()
    assert "Error: formato de datos inesperado." in captured.out


def test_success_prints_temperature(monkeypatch, capsys):
    # Both APIs succeed and valid temperature is printed
    geo = FakeResponse(status_code=200, json_data=[{"lat": "10.0", "lon": "20.0"}])
    weather = FakeResponse(status_code=200, json_data={"current_weather": {"temperature": 20}})
    monkeypatch.setattr("requests.get", make_get_responses([geo, weather]))

    obtener_temperatura("CiudadX")
    captured = capsys.readouterr()
    assert "La temperatura actual en CiudadX es de 20" in captured.out
