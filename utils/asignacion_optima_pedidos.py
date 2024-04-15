import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import scipy as sp
from informacion import pedidos
from utils.geocode_direccion_a_coordenadas import geocode_direccion_a_coordenadas


def calcular_distancia(punto_inicial, arreglo_puntos):
    """Calcula la distancia entre el punto inicial y cada punto en el arreglo de puntos.

    Args:
        punto_inicial (tuple): Coordenadas del punto inicial (latitud, longitud).
        arreglo_puntos (list of tuples): Lista de coordenadas de puntos (latitud, longitud).

    Returns:
        pandas.DataFrame: Un DataFrame que contiene las distancias en kilómetros.
    """
    distancias = [geodesic(punto_inicial, punto).kilometers for punto in arreglo_puntos]
    df_distancias = pd.DataFrame(distancias, columns=["distancia"])
    return df_distancias


def obtener_distancias(direccion_inicio):
    """Obtiene la distancia desde el punto de inicio hasta cada punto de entrega.

    Args:
        direccion_inicio (str): La dirección de inicio del viaje.

    Returns:
        pandas.DataFrame: Un DataFrame que contiene las distancias desde el punto de inicio hasta cada punto de entrega.
    """
    df_pedidos = pedidos()
    direccion_salida = direccion_inicio
    df_direcciones_pedidos = df_pedidos["direccion"]
    df_puntos_pedidos = geocode_direccion_a_coordenadas(
        df_direcciones_pedidos, direccion_salida
    )
    geolocator = Nominatim(user_agent="flutas_geocoder")
    punto_salida = geolocator.geocode(direccion_salida)
    df_distancias = calcular_distancia(
        (punto_salida.latitude, punto_salida.longitude), df_puntos_pedidos.values
    )
    return df_distancias


def obtener_rendimiento_combustible(df_vehiculos):
    """Obtiene el rendimiento de combustible de cada vehículo.

    Args:
        df_vehiculos (pandas.DataFrame): DataFrame que contiene información sobre los vehículos.

    Returns:
        pandas.Series: Una Serie que contiene el rendimiento de combustible de cada vehículo.
    """
    df_rendimiento = df_vehiculos["rendimiento"]
    return df_rendimiento


def obtener_costo_combustible(df_vehiculos):
    """Calcula el costo del combustible para cada tipo de vehículo.

    Args:
        df_vehiculos (pandas.DataFrame): DataFrame que contiene información sobre los vehículos.

    Returns:
        pandas.Series: Una Serie que contiene el costo del combustible para cada tipo de vehículo.
    """
    df_costo_combustible = df_vehiculos["combustible"].copy()
    df_costo_combustible.loc[df_costo_combustible == "gasolina"] = 15000
    df_costo_combustible.loc[df_costo_combustible == "diesel"] = 9500
    df_costo_combustible.loc[df_costo_combustible == "acpm"] = 9500
    df_vehiculos["costo_combustible"] = df_costo_combustible
    return df_costo_combustible


def obtener_costo_viaje(direccion_inicio, df_vehiculos):
    """Calcula el costo del viaje para cada vehículo basándose en la distancia desde el punto de inicio
    hasta cada punto de entrega, el rendimiento de combustible de cada vehículo y el costo del
    combustible.

    Args:
        direccion_inicio (str): La dirección de inicio del viaje.
        df_vehiculos (pandas.DataFrame): DataFrame que contiene información sobre los vehículos.

    Returns:
        numpy.ndarray: Una matriz numpy que contiene el costo del viaje para cada vehículo.
        Matriz mxn, donde la entrada mn es el costo del viaje m-ésimo para el n-ésimo vehículo.
    """
    df_distancias = obtener_distancias(direccion_inicio)
    df_rendimiento_combustible = obtener_rendimiento_combustible(df_vehiculos)
    df_costo_combustible = obtener_costo_combustible(df_vehiculos)
    rendimiento_combustible_np = df_rendimiento_combustible.to_numpy(dtype=float)
    costo_combustible_np = df_costo_combustible.to_numpy(dtype=float)
    costo_kilometro_np = np.divide(
        costo_combustible_np, rendimiento_combustible_np
    ).reshape(-1, 1)
    distancias_np = df_distancias.to_numpy()
    costo_viaje_np = np.matmul(distancias_np, costo_kilometro_np.T)
    return costo_viaje_np


def asignar_vehiculo_a_pedido(direccion_inicio, df_vehiculos):
    """Asigna a cada vehículo un pedido basado en minimizar la suma de los
    costos de viaje de cada vehículo a cada pedido.

    Args:
        direccion_inicio (str): La dirección de inicio del viaje.
        df_vehiculos (pandas.DataFrame): DataFrame que contiene información sobre los vehículos.

    Returns:
        pandas.DataFrame: Un DataFrame que contiene la asignación óptima de vehículos a pedidos, 
        junto con el costo total de la asignación.
    """
    matriz_costos = obtener_costo_viaje(direccion_inicio, df_vehiculos)
    matriz_costos[matriz_costos == 0] = np.inf
    fila_ind, col_ind = sp.optimize.linear_sum_assignment(matriz_costos)
    coste_total = matriz_costos[fila_ind, col_ind].sum()
    df_asignacion_optima =  pd.DataFrame({
        "vehiculo": col_ind,
        "pedido": fila_ind,
        "costo": matriz_costos[fila_ind, col_ind]
    })
    return df_asignacion_optima, coste_total


def main():
    pass

if __name__ == "__main__":
    main()