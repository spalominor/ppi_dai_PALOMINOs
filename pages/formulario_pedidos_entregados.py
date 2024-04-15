import streamlit as st
import pandas as pd
import informacion

def actualizar_estado_pedidos(form_df, df_pedidos):
    """
    Actualiza el estado del pedido en el dataframe de los pedidos.
    """
    id_pedido = form_df['id_pedido'].iloc[0]
    df_pedidos.iloc[id_pedido, df_pedidos.columns.get_loc('estado')] = 'Entregado'
    return df_pedidos
    

def main():
    df_conductores = informacion.conductores()
    df_vehiculos = informacion.vehiculos()
    df_pedidos = informacion.pedidos()
    
    st.title('Registro de Pedido Completado por Conductor')

    # Opciones para los conductores y vehículos
    conductores = df_conductores['nombre'].tolist()
    conductores[0] = 'Conductor'
    vehiculos = df_vehiculos['placa'].tolist()
    vehiculos[0] = 'Vehículo'
    
    # Crear un diccionario para almacenar los datos del formulario
    form_data = {
        "conductor": None,
        "vehiculo": None,
        "fecha_entrega": None,
        "id_pedido": None,
        "hora_entrega": None,
    }

    # Formulario
    with st.form('Registro de Pedido Completado'):
        form_data["conductor"] = st.selectbox('Selecciona el conductor:', conductores)
        form_data["vehiculo"] = st.selectbox('Selecciona el vehículo:', vehiculos)
        form_data["id_pedido"] = st.text_input('Número de ID del pedido:')
        form_data["fecha_entrega"] = st.date_input('Fecha de entrega del pedido')
        
        submitted = st.form_submit_button('Registrar')

    # Procesamiento de los datos ingresados
    if submitted:
        # Agregar la hora actual al DataFrame
        form_data['hora_entrega'] = pd.Timestamp.now().strftime('%H:%M:%S')
        # Crear un DataFrame con los datos del formulario
        form_df = pd.DataFrame([form_data.values()], columns=form_data.keys())
        # Actualizar la información en la base de datos
        informacion.actualizar_informacion('acciones_conductor_pedidos', form_df)
        actualizar_estado_pedidos(form_df, df_pedidos)
        informacion.editar_informacion('pedidos', df_pedidos)
        st.success('¡Pedido completado registrado exitosamente!')

if __name__ == '__main__':
    main()