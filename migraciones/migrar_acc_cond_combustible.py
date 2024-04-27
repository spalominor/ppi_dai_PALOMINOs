import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de DATABASE_URL del entorno
DATABASE_URL = os.getenv('DATABASE_URL')

# Función para migrar las acciones de conductor relacionadas con combustible
def migrar_acciones_combustible():
    """
    Migrar las acciones de conductor relacionadas con combustible desde un 
    archivo CSV a una base de datos PostgreSQL en Heroku.
    
    Args:
        Ninguno
        
    Returns:
        Ninguno
    """
    # Leer los datos del archivo CSV
    df_acciones_combustible = pd.read_csv(
        'bdd/acciones_conductor_combustible.csv')

    # Conectar con la base de datos PostgreSQL en Heroku
    conn = psycopg2.connect(DATABASE_URL)

    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Iterar sobre las filas del DataFrame y ejecutar una consulta SQL 
    # para insertar cada una en la tabla correspondiente
    for index, row in df_acciones_combustible.iterrows():
        cursor.execute("""
            INSERT INTO acc_cond_combustible (
                conductor, vehiculo, galones, kilometraje, 
                fecha, hora, descripcion, propietario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['conductor'],
            row['vehiculo'],
            row['galones'],
            row['kilometraje'],
            row['fecha'],
            row['hora'],
            row['descripcion'],
            row['propietario']
        ))

    # Confirmar los cambios
    conn.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    # Imprimir mensaje de éxito
    print("Migración de acciones de conductor combustible completada.")

# Llamar a la función para migrar las acciones de conductor combustible
migrar_acciones_combustible()
