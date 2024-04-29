# Importamos la librería streamlit
import streamlit as st



# Establecer el nombre de la página
st.set_page_config(page_title='Flutas', page_icon='🍇🛻')


def main():
    """
    Función principal que define la vista inicial de la aplicación.
    
    Args:
        None
        
    Returns:
        None
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

        - Registro de usuarios.
        - Visualizar y filtrar pedidos.
        - Registrar nuevos pedidos.
        """
    )

    # Información personal del desarrollador
    st.header("Información Profesional de Desarrollador")
    st.markdown(
        """
        - **Nombre:** Samuel Palomino Restrepo.
        - **Ubicación:** Medellín, Antioquia.
        - **Información profesional:** Soy bachiller, actualmente estudiante 
        del programa de Ingeniería de
          Sistemas e Informática en la Universidad Nacional - Sede Medellín. 
          Tengo conocimientos en
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
