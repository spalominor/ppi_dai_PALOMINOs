import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import scipy as sp
from data import pedidos, vehiculos


def calcular_distancia(punto_inicial, arreglo_puntos):
    # Calcular la distancia entre el punto inicial y cada punto en el arreglo de puntos
    distancias = [geodesic(punto_inicial, punto).kilometers for punto in arreglo_puntos]
    df_distancias = pd.DataFrame(distancias, columns=["distancia"])
    return df_distancias


def geocode_direccion_a_coordenadas(arreglo_direcciones, si_es_na):
    geolocator = Nominatim(user_agent="flutas_geocoder")
    coordenadas = []
    for direccion in arreglo_direcciones:
        ubicacion = geolocator.geocode(direccion)
        if ubicacion is None:
            ubicacion = geolocator.geocode(si_es_na)
        coordenadas.append(
            {"latitude": ubicacion.latitude, "longitude": ubicacion.longitude}
        )
    df_puntos_codificados = pd.DataFrame(coordenadas)
    return df_puntos_codificados


def obtener_distancias(direccion_inicio):
    # Obtener datos de pedidos
    df_pedidos = pedidos()

    # Dirección de salida
    direccion_salida = direccion_inicio

    # Geocodificar direcciones de pedidos
    df_direcciones_pedidos = df_pedidos["direccion"]
    df_puntos_pedidos = geocode_direccion_a_coordenadas(
        df_direcciones_pedidos, direccion_salida
    )

    # Geocodificar dirección de salida
    geolocator = Nominatim(user_agent="flutas_geocoder")
    punto_salida = geolocator.geocode(direccion_salida)

    # Calcular la distancia entre la dirección de salida y cada punto de entrega
    df_distancias = calcular_distancia(
        (punto_salida.latitude, punto_salida.longitude), df_puntos_pedidos.values
    )
    return df_distancias


def obtener_rendimiento_combustible(df_vehiculos):
    # Obtener datos de vehiculos
    # Obtener el rendimiento del vehículo de la base de datos
    df_rendimiento = df_vehiculos["rendimiento"]
    return df_rendimiento


def obtener_costo_combustible(df_vehiculos):

    # Crear una copia de la columna 'combustible'
    df_costo_combustible = df_vehiculos["combustible"].copy()

    # Asignar valores de costo de combustible basados en el tipo de combustible
    df_costo_combustible.loc[df_costo_combustible == "gasolina"] = 15000
    df_costo_combustible.loc[df_costo_combustible == "diesel"] = 9500
    df_costo_combustible.loc[df_costo_combustible == "acpm"] = 9500

    # Crear una nueva columna 'costo_combustible' con los valores asignados
    df_vehiculos["costo_combustible"] = df_costo_combustible

    return df_costo_combustible


def obtener_costo_viaje(direccion_inicio, df_vehiculos):
    """Calcula el costo del viaje para cada vehículo basándose en la distancia desde el punto de inicio
    hasta cada punto de entrega, el rendimiento de combustible de cada vehículo y el costo del
    combustible.

    Args:
        direccion_inicio (str): La dirección de inicio del viaje.

    Returns:
        Matriz numpy: Una matriz de numpy con el costo del viaje para cada vehículo.
        Matriz mxn, donde la entrada mn es el costo del viaje m-ésimo para el n-ésimo vehículo.
    """
    # Obtener distancia desde el inicio hasta cada punto de entrega
    df_distancias = obtener_distancias(direccion_inicio)

    # Obtener consumo de combustible de cada vehículo
    df_rendimiento_combustible = obtener_rendimiento_combustible(df_vehiculos)

    # Obtener el valor por galón según el tipo de combustible
    df_costo_combustible = obtener_costo_combustible(df_vehiculos)

    # Obtener el costo de cada kilometro a recorrer
    rendimiento_combustible_np = df_rendimiento_combustible.to_numpy(dtype=float)
    costo_combustible_np = df_costo_combustible.to_numpy(dtype=float)
    costo_kilometro_np = np.divide(
        costo_combustible_np, rendimiento_combustible_np
    ).reshape(-1, 1)

    # Calcular el costo total del viaje
    distancias_np = df_distancias.to_numpy()
    costo_viaje_np = np.matmul(distancias_np, costo_kilometro_np.T)
    return costo_viaje_np


def asignar_vehiculo_a_pedido(direccion_inicio, df_vehiculos):
    """ "Asigna a cada vehículo un pedido basado en minimizar la suma de los
    costos de viaje de cada vehículo a cada pedido.

    args:

    return:
    """
    # Obtener matriz de costos. Cada fila representa un pedido y cada columna un vehículo.
    matriz_costos = obtener_costo_viaje(direccion_inicio, df_vehiculos)
    print(matriz_costos.dtype)
    matriz_costos[matriz_costos == 0] = np.inf

    # Asignar el vehículo con menor costo de viaje a cada pedido
    fila_ind, col_ind = sp.optimize.linear_sum_assignment(matriz_costos)

    return fila_ind, col_ind, matriz_costos


def main():
    df_vehiculos = vehiculos()
    direccion_inicio = "Calle 76a Sur #55-29, Antioquia, Colombia"
    fila_ind, col_ind, matriz_costos = asignar_vehiculo_a_pedido(
        direccion_inicio, df_vehiculos
    )
    coste_total = matriz_costos[fila_ind, col_ind].sum()
    print("Asignación de vehículos a pedidos:")
    for f, c in zip(fila_ind, col_ind):
        print(f"Vehículo {c}: Pedido {f}")
    print(coste_total)


if __name__ == "__main__":
    main()