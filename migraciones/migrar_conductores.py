import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de DATABASE_URL del entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Leer los datos del archivo CSV de conductores
df_conductores = pd.read_csv('bdd/conductores.csv')

# Conectar con la base de datos PostgreSQL en Heroku
conn = psycopg2.connect(DATABASE_URL)

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Iterar sobre las filas del DataFrame y ejecutar una consulta SQL 
# para insertar cada una en la tabla conductores
for index, row in df_conductores.iterrows():
    cursor.execute("""
        INSERT INTO conductores (nombre, vehiculo, descripcion, propietario)
        VALUES (%s, %s, %s, %s)
    """, (
        row['nombre'],
        row['vehiculo'],
        row['descripcion'],
        row['propietario']
    ))

# Confirmar los cambios
conn.commit()

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

# Consulta SQL para seleccionar todos los registros de la tabla conductores
sql_select_conductores = """
    SELECT * FROM conductores
"""

# Conectar con la base de datos PostgreSQL para verificar los conductores
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Ejecutar la consulta SQL
cursor.execute(sql_select_conductores)

# Obtener los resultados de la consulta
conductores_registrados = cursor.fetchall()

# Imprimir los resultados
print("Conductores registrados en la base de datos:")
for conductor in conductores_registrados:
    print(conductor)

# Cerrar el cursor y la conexión
cursor.close()
conn.close()
