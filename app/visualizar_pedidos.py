import streamlit as st
import informacion

def main():
    """
    Visualización de pedidos.
    """
    st.title('Visualización de Pedidos')

    # Cargar datos de los pedidos
    df_pedidos = informacion.pedidos()
    opciones_estado = ['Todos', 'Pendiente', 'En camino', 'Entregado']
    
    # Filtrar y ordenar los pedidos si es necesario
    with st.sidebar:
        st.write('## Filtrar y ordenar pedidos')
        activar_tabla_dinamica = st.checkbox('Activar tabla dinámica')

        if activar_tabla_dinamica:
            filtro_estado = st.selectbox('Filtrar por Estado:', opciones_estado)
            if filtro_estado != 'Todos':
                df_pedidos = df_pedidos[df_pedidos['estado'] == filtro_estado]

            busqueda_direccion = st.text_input('Buscar por Dirección:')
            busqueda_cliente = st.text_input('Buscar por cliente:')
            if busqueda_direccion or busqueda_cliente:
                df_pedidos = df_pedidos[
                    df_pedidos['direccion'].str.contains(busqueda_direccion, case=False) & \
                    df_pedidos['cliente'].str.contains(busqueda_cliente, case=False)
                    ]
                
            busqueda_fecha = st.date_input('Buscar por fecha:', value=None)
            if busqueda_fecha is not None:
                df_pedidos = df_pedidos[
                    df_pedidos['fecha'].dt.date == busqueda_fecha
                    ]
            
            orden_columna = st.selectbox('Ordenar por Columna:', df_pedidos.columns)

            # Botones de orden ascendente y descendente
            orden_ascendente = st.button('Orden Ascendente')
            orden_descendente = st.button('Orden Descendente')

            # Ordenar según el botón presionado
            if orden_ascendente:
                df_pedidos = df_pedidos.sort_values(by=orden_columna)
            elif orden_descendente:
                df_pedidos = df_pedidos.sort_values(by=orden_columna, ascending=False)
                

    col_1, col_2 = st.columns([4, 1])
    # Mostrar tabla de pedidos
    with col_1:
        st.write(df_pedidos)
    
    with col_2:
        if st.button('Crear pedidos'):
            st.switch_page('pages/formulario_pedidos.py')

if __name__ == '__main__':
    main()