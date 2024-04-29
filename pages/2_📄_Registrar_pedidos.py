# Importar librerías necesarias
# Importar librerías nativas de Python
import os
import time
# Importar librerías de terceros
import dotenv
import pandas as pd
import psycopg2
import streamlit as st
# Importar funciones necesarias
from utils.usuario import obtener_nombre_usuario



# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")


def registrar_nuevo_pedido(datos_pedido: dict) -> bool:
    """
    Registra un nuevo pedido en la base de datos.
    
    Args:
        datos_pedido (dict): Un diccionario con los datos del pedido.
        
    Returns:
        bool: True si el pedido se registró correctamente, 
        False en caso contrario.
    """
    try:
        # Conectarse a la base de datos
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Obtener el nombre de usuario del usuario
        username = obtener_nombre_usuario()
        
        # Verificar que si se obtuvo el nombre de usuario
        if username is None:
            return False
    
        # Insertar los datos del pedido en la base de datos
        cursor.execute("""
            INSERT INTO pedidos (
                direccion, fecha, cliente, estado, descripcion, propietario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (datos_pedido['direccion_pedido'], datos_pedido['fecha_pedido'], 
            datos_pedido['cliente'], 'Pendiente', 
            datos_pedido['descripcion'], username
            )
        )

        # Commit para confirmar los cambios
        conn.commit()
        
        # Cerrar el cursor
        cursor.close()
        
        # Cerrar la conexión
        conn.close()
        
        # Retornar True si se registró el pedido correctamente
        return True
    except psycopg2.Error as e:
        # Imprimir el error si no se pudo registrar el pedido
        print("Error al registrar el pedido:", e)
        
        # Retornar False si no se pudo registrar el pedido
        return False


def main():
    """
    Función principal que ejecuta la aplicación de registro de nuevo pedido.
    
    Args:
        None
    
    Returns:
        None
    """
    st.title('Registro de Nuevo Pedido')

    # Crear un diccionario para almacenar los datos del formulario
    form_data = {
        "direccion_pedido": None,
        "fecha_pedido": None,
        "cliente": None,
        "estado_pedido": None,
        "descripcion": None
    }

    # Formulario
    with st.form('Registro de Nuevo Pedido'):
        form_data["direccion_pedido"] = st.text_input('Dirección del pedido:')
        form_data["cliente"] = st.text_input('Nombre del cliente:')
        form_data["descripcion"] = st.text_area('Descripción del pedido:')
        submitted = st.form_submit_button('Registrar Pedido')

    # Procesamiento de los datos
    if submitted:
        # Capturar la fecha y hora en la que se registró el pedido
        form_data["fecha_pedido"] = pd.Timestamp.now().strftime(
            '%Y-%m-%d %H:%M:%S')
        # Registrar el nuevo pedido en la base de datos
        if registrar_nuevo_pedido(form_data):
            # Crear un contenedor para mostrar el mensaje de éxito
            success_message = st.empty()
            # Mostrar mensaje de éxito si se registró el pedido correctamente
            success_message.success('¡Pedido registrado exitosamente!')
            # Esperar 3 segundos antes de limpiar el mensaje
            time.sleep(3)
            # Limpiar el mensaje de éxito
            success_message.empty()
        else:
            # Mostrar mensaje de error si no se pudo registrar el pedido
            st.error("""Error al registrar el pedido. 
                     Por favor, inténtalo nuevamente.""")


if __name__ == '__main__':
    # Ejecutar la función principal
    main()
    
