import pandas as pd
from geopy.geocoders import Nominatim
from informacion import actualizar_informacion, geocode_pedidos

geolocator = Nominatim(user_agent="flutas_geocoder")

def geocode_direccion_a_coordenadas(arreglo_direcciones, si_es_na):
    """Convierte una lista de direcciones en coordenadas (latitud, longitud).

    Args:
        arreglo_direcciones (list of str): Lista de direcciones a geocodificar.
        si_es_na (str): Dirección de respaldo en caso de que la dirección no sea encontrada.

    Returns:
        pandas.DataFrame: Un DataFrame que contiene las coordenadas de cada dirección.
    """
    coordenadas = []
    df_geocode_nuevos = pd.DataFrame()
    for direccion in arreglo_direcciones:
        df_geocode_realizados = geocode_pedidos()
        ubicacion = geolocator.geocode(direccion)
        if ubicacion is None:
                ubicacion = geolocator.geocode(si_es_na)
        ya_existe = verificar_si_existe(ubicacion)
        if ya_existe:
            print("Existe")
            coordenadas.append({
                "latitude": df_geocode_realizados['latitude'].loc[ya_existe],
                "longitude": df_geocode_realizados['longitude'].loc[ya_existe]
            })
        else:
            coordenadas.append(
                {"latitude": ubicacion.latitude, "longitude": ubicacion.longitude}
            )
            print("nuevo")
            df_geocode_nuevos = pd.DataFrame({
                    'direccion': ubicacion,
                    'latitude': ubicacion.latitude,
                    'longitude': ubicacion.longitude,
                })
            actualizar_informacion('geocode_pedidos', df_geocode_nuevos)
    df_puntos_codificados = pd.DataFrame(coordenadas)
    return df_puntos_codificados

def verificar_si_existe(ubicacion):
    """Verifica si una dirección ya ha sido geocodificada.

    Args:
        direccion (str): Dirección a verificar.
        df_geocode_realizados (pandas.DataFrame): DataFrame que contiene las coordenadas geocodificadas.

    Returns:
        bool: Indice del lugar de la dirección si la dirección ya ha sido geocodificada
        False en caso contrario.
    """
    df_geocode_realizados = geocode_pedidos()
    if df_geocode_realizados.empty:
        return False
    if ubicacion is None:
        return False
    esta_en_df = df_geocode_realizados['direccion'].isin(ubicacion)
    if esta_en_df.idxmax() != 0:
        print(esta_en_df.idxmax())
        return esta_en_df.idxmax()
    else:
        print(esta_en_df)
        return False