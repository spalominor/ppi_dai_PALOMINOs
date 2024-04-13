import pandas as pd

# Cargar los datos desde los archivos CSV
def vehiculos():
    return pd.read_csv('data/vehiculos.csv', names=['id', 'placa', 'tipo', 'modelo', 'año', 'capacidad', 'kilometraje', 'combustible', 'rendimiento'])

def conductores():
    return pd.read_csv('data/conductores.csv', names=['nombre', 'vehiculo']) 

def pedidos():
    return pd.read_csv('data/pedidos.csv', names=['direccion', 'fecha', 'cliente', 'estado'])

def acciones_conductor_combustible():
    return pd.read_csv('data/acciones_conductor_combustible.csv', names=['conductor', 'vehiculo', 'galones_gasolina', 'kilometraje', 'fecha', 'hora'])

def actualizar_informacion(csvfile, data):
    data.to_csv(f"data/{csvfile}.csv", mode='a', header=False, index=False)

def editar_informacion(csvfile, data):
    data.to_csv(f"data/{csvfile}.csv", index=False, header=False)