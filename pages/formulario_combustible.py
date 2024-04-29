import streamlit as st
import pandas as pd
import informacion


def actualizar_kilometraje(form_df, df_vehiculos):
    """
    Actualiza el kilometraje del vehículo en el dataframe de los vehiculos.
    """
    vehiculo = form_df['vehiculo'].iloc[0]
    kilometraje = form_df['kilometraje'].iloc[0]
    # Actualizar el kilometraje del vehículo
    df_vehiculos.loc[df_vehiculos['placa'] ==
                     vehiculo, 'kilometraje'] = kilometraje
    return df_vehiculos


def actualizar_rendimiento(form_df, df_vehiculos):
    """"
    Actualizar el rendimiento del vehículo en el dataframe de los vehiculos.
    """
    vehiculo = form_df['vehiculo'].iloc[0]
    gasolina = form_df['galones_gasolina'].iloc[0]
    kilometraje = form_df['kilometraje'].iloc[0]
    # Obtener el kilometraje actual del vehículo
    kilometraje_actual = df_vehiculos.loc[df_vehiculos['placa']
                                          == vehiculo, 'kilometraje'].iloc[0]
    rendimiento = (kilometraje - kilometraje_actual) / gasolina
    # Obtener el rendimiento actual del vehículo
    rendimiento_actual = df_vehiculos.loc[df_vehiculos['placa']
                                          == vehiculo, 'rendimiento'].iloc[0]
    if rendimiento == 0:
        return df_vehiculos
    df_vehiculos.loc[df_vehiculos['placa'] == vehiculo, 'rendimiento'] = (
        float(rendimiento_actual) + rendimiento) / 2
    return df_vehiculos


def main():
    df_conductores = informacion.conductores()
    df_vehiculos = informacion.vehiculos()

    st.title('Registro de Información de Conductor')

    conductores = df_conductores['nombre'].tolist()
    vehiculos = df_vehiculos['placa'].tolist()

    form_data = {
        "conductor": None,
        "vehiculo": None,
        "galones_gasolina": None,
        "kilometraje": None,
        "fecha": None,
        "hora": None,
    }

    with st.form('Registro'):
        form_data["conductor"] = st.selectbox(
            'Selecciona el conductor:', conductores)
        form_data["vehiculo"] = st.selectbox(
            'Selecciona el vehículo:', vehiculos)
        form_data["galones_gasolina"] = st.number_input(
            'Galones de gasolina:', min_value=0.0, step=0.1, format="%.3f")
        form_data["kilometraje"] = st.number_input(
            'Kilometraje del vehículo:', min_value=0, step=100)
        form_data["fecha"] = st.date_input('Fecha de la acción')

        submitted = st.form_submit_button('Registrar')

    if submitted:
        form_data['hora'] = pd.Timestamp.now().strftime('%H:%M:%S')
        form_df = pd.DataFrame([form_data])  # No es necesario usar values
        informacion.actualizar_informacion(
            'acciones_conductor_combustible', form_df)
        df_vehiculos = actualizar_rendimiento(form_df, df_vehiculos)
        df_vehiculos = actualizar_kilometraje(form_df, df_vehiculos)
        informacion.editar_informacion('vehiculos', df_vehiculos)
        st.success('¡Información registrada exitosamente!')


if __name__ == '__main__':
    main()

