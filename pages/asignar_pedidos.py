import streamlit as st
from informacion import vehiculos, pedidos
from utils.asignacion_optima_pedidos import asignar_vehiculo_a_pedido


def main():
    st.title("Asignación Óptima de Vehículos a Pedidos")
    
    st.write("Actualmente corriendo en: ")
    st.write("192.168.1.3:8501")

    df_vehiculos = vehiculos()
    df_pedidos = pedidos()

    # Obtener la dirección de inicio del viaje (se puede ingresar desde la
    # interfaz)
    direccion_inicio = st.text_input(
        "Ingrese la dirección de inicio del viaje:")

    if direccion_inicio:
        # Calcular la asignación óptima de vehículos a pedidos
        df_asignacion, coste_total = asignar_vehiculo_a_pedido(
            direccion_inicio, df_vehiculos)
        asignacion = df_asignacion.copy()

        if st.checkbox("Ver información detallada", value=False):
            # Mostrar el DataFrame con la asignación óptima
            st.subheader("Asignación Óptima de Vehículos a Pedidos:")

            asignacion = asignacion.sort_values(
                by='vehiculo')
            for vehiculo in asignacion['vehiculo']:
                asignacion.loc[asignacion['vehiculo'] == vehiculo,
                               'placa'] = df_vehiculos.loc[vehiculo, 
                                                           'placa']
                asignacion.loc[asignacion['vehiculo'] == vehiculo,
                               'modelo'] = df_vehiculos.loc[vehiculo, 
                                                            'modelo']
            for pedido in asignacion['pedido']:
                asignacion.loc[asignacion['pedido'] == pedido,
                               'direccion'] = df_pedidos.loc[pedido, 
                                                             'direccion']
                asignacion.loc[asignacion['pedido'] == pedido,
                               'cliente'] = df_pedidos.loc[pedido, 
                                                           'cliente']
            st.write(asignacion)

        else:
            del asignacion['costo']
            st.write(asignacion)

            # Mostrar el costo total de la asignación
        st.subheader("Costo Total de la Asignación:")
        st.success(int(coste_total))


if __name__ == "__main__":
    main()
