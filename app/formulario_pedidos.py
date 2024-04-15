import streamlit as st
import pandas as pd
import informacion
import time

def main():
    """
    Función principal que ejecuta la aplicación de registro de nuevo pedido.
    """
    st.title('Registro de Nuevo Pedido')

    # Crear un diccionario para almacenar los datos del formulario
    form_data = {
        "direccion_pedido": None,
        "fecha_pedido": None,
        "cliente": None,
        "estado_pedido": None,
    }

    # Formulario
    with st.form('Registro de Nuevo Pedido'):
        form_data["direccion_pedido"] = st.text_input('Dirección del pedido:')
        form_data["cliente"] = st.text_input('Nombre del cliente:')
        form_data["estado_pedido"] = st.selectbox('Estado del pedido:', ['Pendiente', 'En camino', 'Entregado'])

        submitted = st.form_submit_button('Registrar Pedido')

    # Procesamiento de los datos
    if submitted:
        # Capturar la fecha y hora en la que se registró el pedido
        form_data["fecha_pedido"] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        # Crear un DataFrame con los datos del formulario
        form_df = pd.DataFrame([form_data.values()], columns=form_data.keys())
        # Actualizar la información en la base de datos
        informacion.actualizar_informacion('pedidos', form_df)
        # Mostrar mensaje de éxito
        success_message = st.empty()
        success_message.success('¡Pedido registrado exitosamente!')
        # Esperar 3 segundos antes de limpiar el mensaje
        time.sleep(3)
        success_message.empty()

if __name__ == '__main__':
    main()