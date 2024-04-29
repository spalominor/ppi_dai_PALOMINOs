import streamlit as st
from utils import obtener_graficos as og

temas_graficos = ["Pedidos según el día y la hora",
                  "Rendimiento de combustible",
                  "Kilometros recorridos por año",
                  "Kilometraje actual de los vehículos",
                  "Vehículos según el año",
                  "Autonomía de los vehículos",
                  ]


def main():
    st.title("Gráficos")
    st.write("Selecciona el tema que deseas visualizar")
    tipo_grafico = st.selectbox("Selecciona el tema", temas_graficos)
    if tipo_grafico:
        vista(tipo_grafico)


def vista(tipo_grafico):
    if tipo_grafico == "Pedidos según el día y la hora":
        graficar_pedidos()
    elif tipo_grafico == "Rendimiento de combustible":
        graficar_rendimiento_combustible()
    elif tipo_grafico == "Kilometros recorridos por año":
        graficar_kilometros_ano()
    elif tipo_grafico == "Kilometraje actual de los vehículos":
        graficar_kilometraje_vehiculos()
    elif tipo_grafico == "Vehículos según el año":
        graficar_ano_vehiculos()
    elif tipo_grafico == "Autonomía de los vehículos":
        graficar_autonomia_vehiculos()


def graficar_pedidos():
    if st.checkbox("Gráfico de pastel: Pedidos por día"):
        st.write("Pedidos realizados según el día de la semana")
        fig = og.graficar_pastel_pedidos_dia()
        st.pyplot(fig)
    if st.checkbox("Histograma: Pedidos por hora del día"):
        st.write("Pedidos realizados cada dos horas")
        fig = og.graficar_histograma_pedidos_por_hora()
        st.pyplot(fig)


def graficar_kilometros_ano():
    if st.checkbox("Grafico de barras: Kilómetros recorridos por año"):
        st.write("""
            Cantidad de kilómetros en promedio recorridos por año
            por cada vehículo según la antigüedad
            """)
        fig = og.graficar_barras_kilometros_ano()
        st.pyplot(fig)
    elif st.checkbox("Grafico boxplot: Kilómetros recorridos por año"):
        st.write("Distribución de los kilómetros recorridos por año")
        fig = og.graficar_boxplot_kilometros_ano()
        st.pyplot(fig)
    elif st.checkbox("Grafico de dispersión: Kilómetros recorridos por año"):
        st.write("Rendimiento en kilómetros por galón de los vehículos")
        fig = og.graficar_scatter_kilometros_ano()
        st.pyplot(fig)
    elif st.checkbox("Gráfico histograma: Kilómetros recorridos por año"):
        st.write("Distribución de los kilómetros recorridos por año")
        cortes = int(st.text_input("Ingrese el número de cortes", 12))
        fig = og.graficar_histograma_kilometros_ano(cortes)
        st.pyplot(fig)


def graficar_rendimiento_combustible():
    if st.checkbox("Gráfico de barras: Rendimiento de los vehículos"):
        st.write("Rendimiento de los vehículos en kilómetros por litro")
        fig = og.graficar_barras_rendimiento_combustible()
        st.pyplot(fig)
    elif st.checkbox("Grafico boxplot: Rendimiento de los vehículos"):
        st.write("Distribución del rendimiento de los vehículos")
        fig = og.graficar_boxplot_rendimiento_combustible()
        st.pyplot(fig)
    elif st.checkbox("Grafico de dispersión: Rendimiento de los vehículos"):
        st.write("Relación entre la antigüedad y el rendimiento")
        fig = og.graficar_scatter_rendimiento_combustible()
        st.pyplot(fig)


def graficar_kilometraje_vehiculos():
    if st.checkbox("Gráfico de histograma: Kilometraje de los vehículos"):
        st.write("Distribución del kilometraje de los vehículos")
        cortes = int(st.text_input("Ingrese el número de cortes", 12))
        fig = og.graficar_histograma_kilometraje_vehiculos(
            cortes)
        st.pyplot(fig)
    elif st.checkbox("Grafico boxplot: Kilometraje de los vehículos"):
        st.write("Distribución del kilometraje de los vehículos")
        fig = og.graficar_boxplot_kilometraje_vehiculos()
        st.pyplot(fig)


def graficar_ano_vehiculos():
    if st.checkbox("Gráfico de barras: Vehículos por año"):
        st.write("Cantidad de vehículos según el año")
        fig = og.graficar_barras_ano_vehiculos()
        st.pyplot(fig)
    elif st.checkbox("Grafico boxplot: Vehículos por año"):
        st.write("Distribución de los vehículos según el año")
        fig = og.graficar_boxplot_ano_vehiculos()
        st.pyplot(fig)
    elif st.checkbox("Grafico de dispersión: Vehículos por año"):
        st.write("Relación entre el kilometraje y el año de los vehículos")
        fig = og.graficar_scatter_ano_vehiculos()
        st.pyplot(fig)


def graficar_autonomia_vehiculos():
    if st.checkbox("Gráfico de barras: Autonomía de los vehículos"):
        st.write("Cantidad de autonomía de los vehículos")
        fig = og.graficar_barras_autonomia_vehiculos()
        st.pyplot(fig)
    elif st.checkbox("Grafico boxplot: Autonomía de los vehículos"):
        st.write("Distribución de la autonomía de los vehículos")
        fig = og.graficar_boxplot_autonomia_vehiculos()
        st.pyplot(fig)
    elif st.checkbox("Grafico de dispersión: Autonomía de los vehículos"):
        st.write("""
            Relación entre la autonomía y la capacidad de combustible
            de los vehículos
            """)
        fig = og.graficar_scatter_autonomia_vehiculos()
        st.pyplot(fig)


if __name__ == "__main__":
    main()

