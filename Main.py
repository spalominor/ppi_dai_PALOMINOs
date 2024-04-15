import streamlit as st

# Librerias
# Streamlit para la creación de la aplicación web


def main():
    """
    Función principal que define la vista inicial de la aplicación.
    """
    # Título y descripción de la aplicación
    st.title("Gestor de Flotas de Vehículos")
    st.write(
        """
        Bienvenido al Gestor de Flotas de Vehículos.
        Esta aplicación ofrece una solución integral
        para el manejo eficiente y efectivo de flotas
        de vehículos, independientemente de su tamaño.
        Combina análisis de datos, modelado predictivo
        y tecnologías de geocodificación para abordar
        necesidades específicas de la industria del
        transporte, permitiendo a las empresas diferenciarse
        de la competencia.
        """
    )

    # Información sobre la aplicación y sus funcionalidades
    st.header("Funcionalidades Disponibles")
    st.write(
        """
        Hasta el momento, la aplicación ofrece las
        siguientes funcionalidades:

        - Visualizar y filtrar pedidos.
        - Registrar nuevos pedidos.
        - Registrar pedidos entregados.
        - Registrar cuando un conductor va a tanquear combustible.
        - Obtener estadísticas sobre pedidos y vehículos.
        - Obtener gráficos sobre las estadísticas de los pedidos y vehículos.
        - Obtener una recomendación sobre cómo asignar
        los vehículos a los pedidos según el costo mínimo total.
        """
    )

    # Información personal del desarrollador
    st.header("Información Profesional de Desarrollador")
    st.markdown(
        """
        - **Nombre:** Samuel Palomino Restrepo.
        - **Ubicación:** Medellín, Antioquia.
        - **Información profesional:** Soy bachiller, actualmente estudiante del programa de Ingeniería de
          Sistemas e Informática en la Universidad Nacional - Sede Medellín. Tengo conocimientos en
          Python, JavaScript, C# y SQL.
        """
    )

    # Contacto del desarrollador
    st.header("Contacto del Desarrollador")
    st.markdown(
        """
        Puedes contactarme a través de los siguientes medios:

        - **Email:** [spalominor@unal.edu.co](mailto:spalominor@unal.edu.co)
        - **LinkedIn:** [Samuel Palomino](https://www.linkedin.com/in/samuel-palomino-9680352ba/)
        - **GitHub:** [spalominor](https://github.com/spalominor)
        - **Stack Overflow:** [spalominor](https://stackoverflow.com/users/23651826/spalominor)
        """
    )


if __name__ == "__main__":
    main()
