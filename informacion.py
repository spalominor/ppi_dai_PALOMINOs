import pandas as pd
import os

direccion_actual = os.path.dirname(os.path.abspath(__file__))
# Cargar los datos desde los archivos CSV


def vehiculos():
    ruta_archivo = os.path.join(direccion_actual, 'bdd', 'vehiculos.csv')
    return pd.read_csv(ruta_archivo)


def conductores():
    return pd.read_csv('bdd/conductores.csv', names=['nombre', 'vehiculo'])


def pedidos():
    ruta_archivo = os.path.join(direccion_actual, 'bdd', 'pedidos.csv')
    return pd.read_csv(ruta_archivo, names=[
                       'direccion', 'fecha', 'cliente', 'estado'])


def acciones_conductor_combustible():
    ruta_archivo = os.path.join(
        direccion_actual, 'bdd', 'acciones_conductor_combustible.csv')
    return pd.read_csv(
        ruta_archivo,
        names=[
            'conductor',
            'vehiculo',
            'galones_gasolina',
            'kilometraje',
            'fecha',
            'hora'])


def geocode_pedidos():
    return pd.read_csv('bdd/geocode_pedidos.csv',
                       names=['direccion', 'latitude', 'longitude'])


def actualizar_informacion(csvfile, data):
    data.to_csv(f"bdd/{csvfile}.csv", mode='a', header=False, index=False)


def editar_informacion(csvfile, data):
    data.to_csv(f"bdd/{csvfile}.csv", index=False, header=False)
