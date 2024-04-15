import streamlit as st
from informacion import vehiculos, pedidos
from asignacion_optima_pedidos import asignar_vehiculo_a_pedido

def main():
    st.title("Asignación Óptima de Vehículos a Pedidos")
    
    df_vehiculos = vehiculos()
    df_pedidos = pedidos()

    # Obtener la dirección de inicio del viaje (se puede ingresar desde la interfaz)
    direccion_inicio = st.text_input("Ingrese la dirección de inicio del viaje:")

    if direccion_inicio:
        # Calcular la asignación óptima de vehículos a pedidos
        df_asignacion, coste_total = asignar_vehiculo_a_pedido(direccion_inicio, df_vehiculos)
        df_asignacion_optima = df_asignacion.copy()

        if st.checkbox("Ver información detallada", value=False):
            # Mostrar el DataFrame con la asignación óptima
            st.subheader("Asignación Óptima de Vehículos a Pedidos:")
            
            df_asignacion_optima = df_asignacion_optima.sort_values(by='vehiculo')
            for vehiculo in df_asignacion_optima['vehiculo']:
                df_asignacion_optima.loc[df_asignacion_optima['vehiculo'] == vehiculo, 'placa'] = df_vehiculos.loc[vehiculo, 'placa']
                df_asignacion_optima.loc[df_asignacion_optima['vehiculo'] == vehiculo, 'modelo'] = df_vehiculos.loc[vehiculo, 'modelo']
            for pedido in df_asignacion_optima['pedido']:
                df_asignacion_optima.loc[df_asignacion_optima['pedido'] == pedido, 'direccion'] = df_pedidos.loc[pedido, 'direccion']
                df_asignacion_optima.loc[df_asignacion_optima['pedido'] == pedido, 'cliente'] = df_pedidos.loc[pedido, 'cliente']
            st.write(df_asignacion_optima)

        else:
            del df_asignacion_optima['costo']
            st.write(df_asignacion_optima)

            # Mostrar el costo total de la asignación
        st.subheader("Costo Total de la Asignación:")
        st.success(int(coste_total))

if __name__ == "__main__":
    main()