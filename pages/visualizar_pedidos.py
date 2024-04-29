import streamlit as st
import informacion
from utils.usuario import username


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

    # Cargar datos de los pedidos
    df_pedidos = informacion.pedidos()

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
                df_pedidos = df_pedidos[df_pedidos['fecha'].str.contains(
                    str(bsq_fecha), case=False)]

            orden_columna = st.selectbox(
                'Ordenar por Columna:',
                ['id'] +
                list(
                    df_pedidos.columns))

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
        if df_pedidos.empty:
            # Mostrar mensaje de error si no hay pedidos
            st.error('No hay pedidos para mostrar')
            # Si la busqueda arroja resultados, entonces:
        elif not df_pedidos.empty:
            # Mostrar tabla de pedidos filtrada y ordenada
            st.write(df_pedidos)
            
            # Mostrar mensaje de éxito si se cargaron los pedidos
            st.success('Pedidos cargados correctamente')
    else:
        # Mostrar tabla de pedidos sin filtrar ni ordenar
        st.write('Tabla dinámica desactivada')
        
        # Eliminar columnas innecesarias
        del df_pedidos['cliente']
        
        # Eliminar columna fecha
        del df_pedidos['fecha']
        
        # Mostrar tabla de pedidos
        st.write(df_pedidos)

    # Botón para redireccionar al formulario para crear pedidos
    if st.button('Crear pedidos'):
        # Redireccionar al formulario de pedidos
        st.switch_page('pages/formulario_pedidos.py')


if __name__ == '__main__':
    # Llamar a la función principal
    main()
