import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de DATABASE_URL del entorno
DATABASE_URL = os.getenv('DATABASE_URL')

def migrar_acciones_pedidos():
    """
    Migrar las acciones de conductor relacionadas con pedidos desde un archivo 
    CSV a una base de datos PostgreSQL en Heroku.
    
    Args:
        Ninguno
        
    Returns:
        Ninguno
    """
    # Leer los datos del archivo CSV
    df_acciones_pedidos = pd.read_csv('bdd/acciones_conductor_pedidos.csv')

    # Conectar con la base de datos PostgreSQL en Heroku
    conn = psycopg2.connect(DATABASE_URL)

    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    try:
        # Iterar sobre las filas del DataFrame y ejecutar una consulta SQL 
        # para insertar cada una en la tabla correspondiente
        for index, row in df_acciones_pedidos.iterrows():
            cursor.execute("""
                INSERT INTO acc_cond_pedidos (
                    conductor, vehiculo, fecha, hora, 
                    pedido, descripcion, propietario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['conductor'],
                row['vehiculo'],
                row['fecha'],
                row['hora'],
                row['pedido'],
                row['descripcion'],
                row['propietario']
            ))

        # Confirmar los cambios
        conn.commit()

        print("Migración de acciones conductor pedidos completada.")

    except psycopg2.Error as e:
        print("Error al migrar acciones conductor pedidos:", e)

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

# Llamar a la función para migrar las acciones de conductor pedidos
migrar_acciones_pedidos()
