import streamlit as st
import numpy as np
import pandas as pd
from informacion import vehiculos, pedidos

# Obtener los datos
df_vehiculos = vehiculos()
df_pedidos = pedidos()

# Días de la semana en español
# Diccionario usado en la función mostrar_estadisticas_pedidos
dias_en_espanol = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}


def mostrar_estadisticas_rendimiento_combustible():
    """
    Mostrar las estadísticas de rendimiento de combustible.
    """
    # Encabezado principal
    st.header("Estadísticas de Rendimiento de Combustible")

    # Indicar la unidad de medida del rendimiento
    st.write("Rendimiento medido en kilómetros por galón (km/gal)")

    # Obtener el rendimiento de combustible de todos los vehículos
    rendimiento_np = df_vehiculos["rendimiento"].to_numpy(dtype="float")

    # Calcular el rendimiento mínimo
    rendimiento_min = np.amin(rendimiento_np)
    # Obtener el vehículo con menor rendimiento
    vehiculo_rendimiento_min = df_vehiculos.loc[
        np.argmin(rendimiento_np), ["placa", "modelo", "año"]
    ]
    st.write(f"- Rendimiento mínimo: {rendimiento_min} km/gal")
    st.write("Vehículo con menor rendimiento:")
    st.write(vehiculo_rendimiento_min)

    # Calcular el rendimiento máximo
    rendimiento_max = np.amax(rendimiento_np)
    # Obtener el vehículo con mayor rendimiento
    vehiculo_rendimiento_max = df_vehiculos.loc[
        np.argmax(rendimiento_np), ["placa", "modelo", "año"]
    ]
    st.write(f"- Rendimiento máximo: {rendimiento_max} km/gal")
    st.write("Vehículo con mayor rendimiento:")
    st.write(vehiculo_rendimiento_max)

    # Calcular el rendimiento promedio
    rendimiento_promedio = round(np.mean(rendimiento_np), 2)
    st.write(f"- Rendimiento promedio: {rendimiento_promedio} km/gal")

    # Calcular la mediana del rendimiento
    rendimiento_mediana = round(np.median(rendimiento_np), 2)
    st.write(f"- Mediana del rendimiento: {rendimiento_mediana} km/gal")

    # Calcular la desviación estándar del rendimiento
    rendimiento_desviacion_estandar = round(np.std(rendimiento_np), 2)
    st.write(
        f"""- Desviación estándar del
        rendimiento: {rendimiento_desviacion_estandar} km/gal"""
    )


def mostrar_estadisticas_autonomia_vehiculos():
    """
    Mostrar las estadísticas de autonomía de los vehículos.
    """
    # Encabezado principal
    st.header("Estadísticas de Autonomía de los Vehículos")

    # Calcular la autonomía de cada vehículo multiplicando la capacidad del
    # tanque por el rendimiento
    autonomia_np = df_vehiculos["capacidad"].to_numpy(
        dtype="float") * df_vehiculos["rendimiento"].to_numpy(dtype="float")

    # Indicar la unidad de medida y explicar qué es la autonomía
    st.write("Autonomía medida en kilómetros (km)")
    st.write(
        """Distancia máxima aproximada que puede recorrer un
        vehículo con un tanque de combustible lleno."""
    )
    st.write(
        """La autonomía se calcula multiplicando la capacidad del tanque de
        combustible por el rendimiento del vehículo."""
    )

    # Calcular y mostrar la autonomía mínima
    autonomia_min = int(np.amin(autonomia_np))
    st.write(f"- Autonomía mínima: {autonomia_min}km")
    vehiculo_autonomia_min = df_vehiculos.loc[
        np.argmin(autonomia_np), ["placa", "modelo", "año"]
    ]
    st.write("Vehículo con menor autonomía:")
    st.write(vehiculo_autonomia_min)

    # Calcular y mostrar la autonomía máxima
    autonomia_max = int(np.amax(autonomia_np))
    st.write(f"- Autonomía máxima: {autonomia_max}")
    vehiculo_autonomia_max = df_vehiculos.loc[
        np.argmax(autonomia_np), ["placa", "modelo", "año"]
    ]
    st.write("Vehículo con mayor autonomía:")
    st.write(vehiculo_autonomia_max)

    # Calcular y mostrar la autonomía promedio
    autonomia_promedio = round(np.mean(autonomia_np), 2)
    st.write(f"- Autonomía promedio: {autonomia_promedio} km.")

    # Calcular y mostrar la mediana de la autonomía
    autonomia_mediana = round(np.median(autonomia_np), 2)
    st.write(f"- Autonomía mediana: {autonomia_mediana} km.")

    # Calcular y mostrar la desviación estándar de la autonomía
    autonomia_desviacion_estandar = round(np.std(autonomia_np), 2)
    st.write(
        f"""- Autonomía desviación
        estándar: {autonomia_desviacion_estandar} km.""")


def mostrar_estadisticas_estado_vehiculos():
    """
    Mostrar estadísticas del estado de los vehículos, incluyendo
    número de vehículos por año, kilometraje y kilómetros recorridos por año.
    """
    # Encabezado principal
    st.header("Estadísticas del Estado de los Vehículos")

    # Número de vehículos por año
    ano_vehiculos_np = df_vehiculos["año"].to_numpy()
    # Contar el numero de vehiculos por cada año
    vehiculo_ano_frecuencia = np.unique(ano_vehiculos_np, return_counts=True)
    # Imprimir el resultado
    st.subheader("Número de Vehículos por Año")
    for ano_vehiculo, frecuencia_ano in zip(
        vehiculo_ano_frecuencia[0], vehiculo_ano_frecuencia[1]
    ):
        st.write(f"- Año {ano_vehiculo}: {frecuencia_ano} vehículos	")

    # Sección 1:
    # Estadísticas de kilometraje
    st.subheader("Estadísticas de Kilometraje")

    # Obtener el kilometraje de todos los vehículos
    kilometraje_vehiculos_np = df_vehiculos["kilometraje"].to_numpy()

    # Calcular el menor kilometraje
    kilometraje_min = np.amin(kilometraje_vehiculos_np)
    st.write(f"Menor Kilometraje: {kilometraje_min}km")

    # Obtener información del vehículo con el menor kilometraje
    vehiculo_kilometraje_min = df_vehiculos.loc[
        np.argmin(kilometraje_vehiculos_np), ["placa", "modelo", "año"]
    ]
    st.write("Vehículo con Menor Kilometraje:")
    st.write(vehiculo_kilometraje_min)

    # Calcular el mayor kilometraje
    kilometraje_max = np.amax(kilometraje_vehiculos_np)
    st.write(f"Mayor Kilometraje: {kilometraje_max}km")

    # Obtener información del vehículo con el mayor kilometraje
    vehiculo_kilometraje_max = df_vehiculos.loc[
        np.argmax(kilometraje_vehiculos_np), ["placa", "modelo", "año"]
    ]
    st.write("Vehículo con Mayor Kilometraje:")
    st.write(vehiculo_kilometraje_max)

    # Calcular el kilometraje promedio
    kilometraje_promedio = round(np.mean(kilometraje_vehiculos_np), 2)
    st.write(f"Kilometraje Promedio: {kilometraje_promedio} km")

    # Calcular la mediana del kilometraje
    kilometraje_mediana = np.median(kilometraje_vehiculos_np)
    st.write(f"Mediana del Kilometraje: {kilometraje_mediana} km")

    # Calcular la desviación estándar del kilometraje
    kilometraje_desviacion_estandar = round(
        np.std(kilometraje_vehiculos_np), 2)
    st.write(
        f"""Desviación Estándar del
        Kilometraje: {kilometraje_desviacion_estandar} km"""
    )

    # Sección 2:
    # Kilómetros recorridos por año
    st.subheader("Kilómetros Recorridos por Año")

    # Calcular años desde el año actual hasta el año del vehículo
    ano_vehiculos_np = (df_vehiculos["año"].to_numpy() - 2024) * -1

    # Calcular los kilómetros recorridos por año
    kilometros_ano_vehiculos_np = kilometraje_vehiculos_np / ano_vehiculos_np

    # Calcular la estadística del menor kilometraje recorrido por año
    kilometros_ano_min = np.amin(kilometros_ano_vehiculos_np)
    st.write(f"Menos Kilómetros Recorridos por Año: {kilometros_ano_min}km")
    vehiculo_kilometros_ano_min = df_vehiculos.loc[
        np.argmin(kilometros_ano_vehiculos_np), ["placa", "modelo", "año"]
    ]
    st.write("Vehículo con Menos Kilómetros Recorridos por Año:")
    st.write(vehiculo_kilometros_ano_min)

    # Calcular la estadística del mayor kilometraje recorrido por año
    kilometros_ano_max = np.amax(kilometros_ano_vehiculos_np)
    st.write(f"Más Kilómetros Recorridos por Año: {kilometros_ano_max} km")
    vehiculo_kilometros_ano_max = df_vehiculos.loc[
        np.argmax(kilometros_ano_vehiculos_np), ["placa", "modelo", "año"]
    ]
    st.write("Vehículo con Más Kilómetros Recorridos por Año:")
    st.write(vehiculo_kilometros_ano_max)

    # Calcular la estadística del promedio de kilómetros recorridos por año
    kilometros_ano_promedio = round(np.mean(kilometros_ano_vehiculos_np), 2)
    st.write(
        f"""Promedio de Kilómetros Recorridos por
        Año: {kilometros_ano_promedio} km""")

    # Calcular la mediana de los kilómetros recorridos por año
    kilometros_ano_mediana = round(np.median(kilometros_ano_vehiculos_np), 2)
    st.write(
        f"""Mediana de los Kilómetros Recorridos por
        Año: {kilometros_ano_mediana} km"""
    )

    # Calcular la desviación estándar de los kilómetros recorridos por año
    kilometros_ano_desviacion_estandar = round(
        np.std(kilometros_ano_vehiculos_np))
    st.write(
        f"""
        Desviación Estándar de los Kilómetros
        Recorridos por Año: {kilometros_ano_desviacion_estandar} km
        """
    )


def mostrar_estadisticas_pedidos():
    """
    Mostrar las estadísticas de los pedidos.

    Args:
    - df_pedidos (pd.DataFrame): DataFrame que contiene los
    datos de los pedidos.
    - dias_en_espanol (dict): Diccionario que mapea nombres
    de días en inglés a español.

    Returns:
    None
    """
    # Mostrar el encabezado
    st.header("Estadísticas de Pedidos")

    # Dividir la columna 'fecha' en fecha y hora
    df_fecha_hora = df_pedidos["fecha"].str.split(" ", expand=True)

    # Mostrar la frecuencia de pedidos por día de la semana
    st.subheader("Frecuencia de Pedidos por Día de la Semana:")

    # Obtener el nombre del día de la semana para cada pedido
    dia_semana_pedido_np = pd.to_datetime(
        df_fecha_hora[0]).dt.day_name().to_numpy()

    # Calcular la frecuencia de pedidos para cada día de la semana
    dia_semana, frecuencia_dia_semana = np.unique(
        dia_semana_pedido_np, return_counts=True
    )

    # Crear un diccionario para mapear los nombres de los días a su frecuencia
    frecuencia_por_dia = dict(zip(dia_semana, frecuencia_dia_semana))

    # Ordenar los días de la semana en el orden correcto
    dias_semana_orden = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Organizar las frecuencias de pedidos por día según el orden de los días
    dia_frecuencia_ordenado = [
        (dias_en_espanol[dia], frecuencia_por_dia.get(dia, 0))
        for dia in dias_semana_orden
    ]

    # Mostrar la frecuencia de pedidos por día de la semana en orden
    for dia, frecuencia in dia_frecuencia_ordenado:
        st.write(f"- {dia}: {frecuencia}")

    # Calcular la mediana de los datos de pedidos según el día de la semana

    # Crear una lista con todos los días de la semana ordenados según la
    # frecuencia de pedidos
    pedidos_por_dia_semana_ordenado = []
    for dia, frecuencia in dia_frecuencia_ordenado:
        for i in range(frecuencia):
            pedidos_por_dia_semana_ordenado.append(dia)

    # Calcular la cantidad total de pedidos
    cantidad_pedidos = len(df_pedidos["fecha"])

    # Calcular la ubicación de la mediana dependiendo de si la cantidad de
    # pedidos es par o impar
    if cantidad_pedidos % 2 == 0:
        ubicacion_mediana = cantidad_pedidos // 2
        mediana_dia_semana = pedidos_por_dia_semana_ordenado[ubicacion_mediana]
    elif cantidad_pedidos % 2 == 1:
        ubicacion_mediana = int(cantidad_pedidos / 2) + 1
        mediana_dia_semana = pedidos_por_dia_semana_ordenado[ubicacion_mediana]

    # Mostrar la mediana de pedidos por día de la semana
    st.write(f"Mediana de Pedidos por Día de la Semana: {mediana_dia_semana}")

    # Sección 2:
    # Mostrar la frecuencia de pedidos por hora del día
    st.subheader("Frecuencia de Pedidos por Hora:")

    # Definir los rangos de hora
    df_rango_hora = pd.Series(
        pd.date_range("00:00", "23:59", freq="2H")
    ).dt.hour.to_numpy()
    df_rango_hora = np.append(df_rango_hora, 24)

    # Obtener la hora de cada pedido
    hora_pedido_np = pd.Series(pd.to_datetime(
        df_fecha_hora[1])).dt.hour.to_numpy()

    # Calcular el histograma de frecuencia de pedidos por hora
    hora_pedido_histograma_np = np.histogram(
        hora_pedido_np, bins=df_rango_hora)

    # Mostrar la frecuencia de pedidos por hora
    for frecuencia, rango_hora in zip(
        hora_pedido_histograma_np[0], hora_pedido_histograma_np[1]
    ):
        st.write(f"- {rango_hora}:00 a {rango_hora + 2}:00: {frecuencia}")

    # Calcular la hora promedio en la que se hacen los pedidos
    df_fecha_hora[0] = np.datetime64("2000-01-01")
    df_temporal_fechas = pd.DataFrame(df_fecha_hora, dtype=str)
    df_temporal_fechas[2] = df_temporal_fechas[0] + " " + df_temporal_fechas[1]
    df_temporal_fechas[3] = np.datetime64("2000-01-01 00:00:00")
    df_temporal_fechas[4] = df_temporal_fechas[2].astype(
        "datetime64[s]"
    ) - df_temporal_fechas[3].astype("datetime64[s]")
    prom = np.mean(df_temporal_fechas[4].dt.total_seconds())
    hora_promedio_segundos_np = np.array(prom).astype("datetime64[s]")
    hora_promedio_np = str(hora_promedio_segundos_np.astype(
        "datetime64[s]")).split("T")[1]
    st.write(
        f"Hora promedio en la que se hacen los pedidos: {hora_promedio_np}")


def mostrar_explicacion_estadisticas():
    """
    Mostrar la explicación de las estadísticas.

    Args:
    - None

    Returns:
    None
    """
    # Mostrar el encabezado
    st.header("Explicación de las Estadísticas")

    # Mostrar la explicación de las estadísticas
    st.write("""
        Las estadísticas incluyen información sobre el
        rendimiento de combustible, la autonomía de los
        vehículos, los pedidos y el estado de los vehículos.
    """)

    st.subheader("¿Qué significa cada estadística?")

    st.write("- Frecuencia")
    st.write("""
        Indica la cantidad de veces que ocurre un evento
        dentro de un conjunto de datos. Por ejemplo, la
        frecuencia de pedidos por día de la semana indica
        cuántos pedidos se realizan en cada día de la semana.
    """)

    st.write("- Promedio")
    st.write("""
        Es la medida central que representa el valor típico
        o central de un conjunto de datos. Se calcula sumando
        todos los valores y dividiéndolos por la cantidad total
        de valores. Por ejemplo, el promedio del kilometraje
        de los vehículos indica la cantidad promedio de kilómetros
        que recorren los vehículos.
    """)

    st.write("- Mediana")
    st.write("""
        Es el valor que se encuentra en el medio de un conjunto
        de datos cuando estos están ordenados de menor a mayor.
        Es una medida de la tendencia central que no se ve
        afectada por valores extremos. Por ejemplo, la mediana
        del kilometraje de los vehículos indica el valor que se
        encuentra en el medio de todos los valores de kilometraje.
    """)

    st.write("- Valor mínimo")
    st.write("""
        Es el valor más pequeño dentro de un conjunto de datos.
        Por ejemplo, el valor mínimo del rendimiento de combustible
        indica el rendimiento más bajo entre todos los vehículos.
    """)

    st.write("- Valor máximo")
    st.write("""
        Es el valor más grande dentro de un conjunto de datos.
        Por ejemplo, el valor máximo del rendimiento de combustible
        indica el rendimiento más alto entre todos los vehículos.
    """)

    st.write("- Desviación estándar")
    st.write("""
        Es una medida de dispersión que indica cuánto varían los
        valores de un conjunto de datos alrededor del promedio. Una
        desviación estándar baja indica que los valores están cerca
        del promedio, mientras que una desviación estándar alta
        indica que los valores están más dispersos. Por ejemplo,
        una baja desviación estándar en el rendimiento de combustible
        indica que la mayoría de los vehículos tienen un rendimiento
        similar, mientras que una alta desviación estándar indica que
        hay una variabilidad significativa en el rendimiento entre
        los vehículos.
    """)

    st.subheader("¿Entiendes más con gráficos?")
    st.write("""
        Visita la pestaña de 'Gráficos' para ver visualizaciones
        de las estadísticas.
    """)


# Opciones del selectbox
opciones = [
    "Rendimiento de Combustible",
    "Autonomía de Vehículos",
    "Pedidos",
    "Estado de Vehículos",
    "¿Qué son estas estadísticas?",
]

# Mostrar el selectbox
tema_seleccionado = st.selectbox("Seleccione un tema:", opciones)

# Mostrar las estadísticas según el tema seleccionado
if tema_seleccionado == "Rendimiento de Combustible":
    mostrar_estadisticas_rendimiento_combustible()
elif tema_seleccionado == "Autonomía de Vehículos":
    mostrar_estadisticas_autonomia_vehiculos()
elif tema_seleccionado == "Pedidos":
    mostrar_estadisticas_pedidos()
elif tema_seleccionado == "Estado de Vehículos":
    mostrar_estadisticas_estado_vehiculos()
elif tema_seleccionado == "¿Qué son estas estadísticas?":
    mostrar_explicacion_estadisticas()

