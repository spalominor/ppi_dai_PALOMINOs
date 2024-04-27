import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de DATABASE_URL del entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Leer los datos del archivo CSV de pedidos
df_pedidos = pd.read_csv('bdd/pedidos.csv')

# Conectar con la base de datos PostgreSQL en Heroku
conn = psycopg2.connect(DATABASE_URL)

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Iterar sobre las filas del DataFrame y ejecutar una consulta SQL 
# para insertar cada una en la tabla pedidos
for index, row in df_pedidos.iterrows():
    cursor.execute("""
        INSERT INTO pedidos (
            direccion, fecha, cliente, estado, 
            descripcion, propietario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row['direccion'],
        row['fecha'],
        row['cliente'],
        row['estado'],
        row['descripcion'],
        row['propietario']
    ))

# Confirmar los cambios
conn.commit()

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

# Consulta SQL para seleccionar todos los registros de la tabla pedidos
sql_select_pedidos = """
    SELECT * FROM pedidos
"""

# Conectar con la base de datos PostgreSQL para verificar los pedidos
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Ejecutar la consulta SQL
cursor.execute(sql_select_pedidos)

# Obtener los resultados de la consulta
pedidos_registrados = cursor.fetchall()

# Imprimir los resultados
print("Pedidos registrados en la base de datos:")
for pedido in pedidos_registrados:
    print(pedido)

# Cerrar el cursor y la conexión
cursor.close()
conn.close()
