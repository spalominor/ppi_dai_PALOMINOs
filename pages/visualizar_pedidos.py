# Importar las librerías nativas necesarias
import os

# Importar las librerías de terceros necesarias
import dotenv
import pandas as pd
import psycopg2
import streamlit as st

# Importar las funciones necesarias para obtener el nombre de usuario
from utils.usuario import obtener_nombre_usuario



# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")


def obtener_pedidos_por_usuario(username: str):
    """
    Obtiene los pedidos asociados al nombre de usuario desde la base de datos.
    
    Args:
        username (str): El nombre de usuario del usuario.

    Returns:
        list: Una lista de tuplas con los datos de los pedidos.
    """
    # Conectarse a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        # Consultar los pedidos asociados al nombre de usuario
        cursor.execute("SELECT * FROM pedidos WHERE propietario = %s", 
                       (username,))
        pedidos = cursor.fetchall()
        return pedidos
    except psycopg2.Error as e:
        print("Error al obtener los pedidos:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def main():
    """
    Define la vista de la página de visualización de pedidos.
    Visualización en forma de dataframe de los pedidos registrados
    en la base de datos a nombre del usuario
    
    Args:
        None
    
    Returns:
        None
    """
    # Establecer el título de la página
    st.title('Visualización de Pedidos')

    # Obtener el nombre de usuario del usuario
    username = obtener_nombre_usuario()
    
    # Cargar datos de los pedidos asociados al usuario
    df_pedidos = pd.DataFrame(obtener_pedidos_por_usuario(username=username),
                              columns=['id', 
                                       'direccion', 
                                       'fecha', 
                                       'cliente', 
                                       'estado', 
                                       'descripcion',
                                       'propietario'])
        
    # Opciones de filtrado y ordenamiento
    opciones_estado = ['Todos', 'Pendiente', 'En camino', 'Entregado']

    # Filtrar y ordenar los pedidos si es necesario
    with st.sidebar:
        # Establecer el título del sidebar
        st.write('## Filtrar y ordenar pedidos')
        
        # Establecer el checkbox para activar la tabla dinámica
        activar_tabla_dinamica = st.checkbox('Activar tabla dinámica')

        if activar_tabla_dinamica:
            filtro_estado = st.selectbox(
                'Filtrar por Estado:', opciones_estado)
            if filtro_estado != 'Todos':
                df_pedidos = df_pedidos[df_pedidos['estado'] == filtro_estado]

            bsq_direccion = st.text_input('Buscar por Dirección:')
            bsq_cliente = st.text_input('Buscar por cliente:')
            if bsq_direccion or bsq_cliente:
                df_pedidos = df_pedidos[
                    df_pedidos['direccion'].str.contains(bsq_direccion,
                                                         case=False) &
                    df_pedidos['cliente'].str.contains(bsq_cliente,
                                                       case=False)
                ]

            bsq_fecha = st.date_input('Buscar por fecha:', value=None)
            if bsq_fecha is not None:
                st.write('Fecha seleccionada:', bsq_fecha)
                df_pedidos = df_pedidos[
                    df_pedidos['fecha'].dt.date == bsq_fecha]

            orden_columna = st.selectbox(
                'Ordenar por Columna:', 
                list(df_pedidos.drop('propietario', axis=1).columns)
            )

            # Botones de orden ascendente y descendente
            orden_ascendente = st.checkbox('Orden Ascendente', value=True)

            # Ordenar según el botón presionado
            if orden_columna:
                if orden_columna == 'id':
                    if orden_ascendente:
                        df_pedidos = df_pedidos.sort_index()
                    elif not orden_ascendente:
                        df_pedidos = df_pedidos.sort_index(ascending=False)
                else:
                    if orden_ascendente:
                        df_pedidos = df_pedidos.sort_values(by=orden_columna)
                    elif not orden_ascendente:
                        df_pedidos = df_pedidos.sort_values(
                            by=orden_columna, ascending=False)

    if activar_tabla_dinamica:
        # Mostrar el título tabla de pedidos
        st.write('Tabla dinámica activada')
        
        # Definir que mostrar si el dataframe está vacío o no:
        if df_pedidos is None or len(df_pedidos) == 0:
            # Mostrar mensaje de error si no hay pedidos
            st.error('No hay pedidos para mostrar')
            # Si la busqueda arroja resultados, entonces:
        elif not df_pedidos.empty:
            # Mostrar tabla de pedidos filtrada, ordenada y con estilo
            st.dataframe(
                df_pedidos.drop('propietario', axis=1),
                column_config={
                    'id': 'ID #️⃣',
                    'direccion': 'Dirección de entrega 🧭',
                    'fecha': 'Fecha 🗓️',
                    'cliente': 'Cliente 🧑',
                    'estado': 'Estado 🚚',
                    'descripcion': 'Descripción 📝',
                    },
                hide_index=True,
                use_container_width=True
            )
            
            # Mostrar mensaje de éxito si se cargaron los pedidos
            st.success('Pedidos cargados correctamente')
    else:
        # Mostrar tabla de pedidos sin filtrar ni ordenar
        st.write('Tabla dinámica desactivada')
        
        if not df_pedidos.empty:
            # Eliminar columnas innecesarias
            df_pedidos.drop(['fecha', 'cliente', 'descripcion','propietario'], 
                            axis=1, 
                            inplace=True)
            # Mostrar tabla de pedidos
            st.dataframe(df_pedidos, hide_index=True)
        else:
            # Mostrar mensaje de error si no hay pedidos
            st.error('No tienes pedidos para mostrar')
        
    # Botón para redireccionar al formulario para crear pedidos
    if st.button('Crear pedidos'):
        # Redireccionar al formulario de pedidos
        st.switch_page('pages/formulario_pedidos.py')


if __name__ == '__main__':
    # Llamar a la función principal
    main()
