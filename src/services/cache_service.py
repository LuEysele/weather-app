cache_coordenadas = {}

def get_cached_coords(ciudad):
    return cache_coordenadas.get(ciudad)

def set_cached_coords(ciudad, lat, lon):
    cache_coordenadas[ciudad] = (lat, lon)