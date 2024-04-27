import os
import psycopg2
from dotenv import load_dotenv

from informacion import vehiculos

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer los datos del archivo CSV
df_vehiculos = vehiculos()

# Obtener el valor de DATABASE_URL del entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Conectar con la base de datos PostgreSQL en Heroku
conn = psycopg2.connect(DATABASE_URL)

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Iterar sobre las filas del DataFrame y ejecutar una consulta SQL 
# para insertar cada una en la tabla vehiculos
for index, row in df_vehiculos.iterrows():
    cursor.execute("""
        INSERT INTO vehiculos (
            placa, tipo, marca, modelo,
            capacidad, kilometraje, combustible, rendimiento, 
            descripcion, propietario
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        row['placa'],
        row['tipo'],
        row['modelo'],
        row['anio'],
        row['capacidad'],
        row['kilometraje'],
        row['combustible'],
        row['rendimiento'],
        row['descripcion'],
        row['propietario']
    ))

# Confirmar los cambios
conn.commit()

# Cerrar el cursor y la conexión
cursor.close()
conn.close()
