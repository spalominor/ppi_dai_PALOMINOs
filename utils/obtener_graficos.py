import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import linregress

from informacion import vehiculos, pedidos

# Cargar los datos de los vehículos
df_vehiculos = vehiculos()
# Cargar los datos de los pedidos
df_pedidos = pedidos()


def graficar_barras_rendimiento_combustible():
    """
    Mostrar las estadísticas de rendimiento de combustible.
    """
    # Encabezado principal

    # Indicar la unidad de medida del rendimiento

    # Obtener el rendimiento de combustible de todos los vehículos
    rendimiento_np = df_vehiculos["rendimiento"].to_numpy(dtype="float")
    vehiculos_np = df_vehiculos["placa"].to_numpy(dtype="str")

    indice_min = np.argmin(rendimiento_np)
    indice_max = np.argmax(rendimiento_np)

    # Calcular el rendimiento promedio
    rendimiento_promedio = round(np.mean(rendimiento_np), 2)

    # Calcular la mediana del rendimiento
    rendimiento_mediana = round(np.median(rendimiento_np), 2)

    # Calcular la desviación estándar del rendimiento

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.bar(
        vehiculos_np,
        rendimiento_np,
        color='skyblue',
        edgecolor='black',
        alpha=0.7)
    plt.axhline(
        rendimiento_promedio,
        color='red',
        linestyle='dashed',
        linewidth=1,
        label='Media')
    plt.axhline(
        rendimiento_mediana,
        color='green',
        linestyle='dashed',
        linewidth=1,
        label='Mediana')
    plt.title('Distribución de Rendimiento de Combustible')
    plt.xlabel('Vehículo (placa)')
    plt.ylabel('Rendimiento (km/gal)')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True)
    plt.annotate(f'Menor: {min(rendimiento_np)} km/gal',
                 xy=(indice_min,
                     min(rendimiento_np)),
                 xytext=(indice_min + 2,
                         min(rendimiento_np) + 3),
                 arrowprops=dict(facecolor='red',
                                 shrink=0.05))
    plt.annotate(f'Mayor: {max(rendimiento_np)} km/gal',
                 xy=(indice_max,
                     max(rendimiento_np)),
                 xytext=(indice_max + 2,
                         max(rendimiento_np) + 3),
                 arrowprops=dict(facecolor='green',
                                 shrink=0.05))
    plt.ylim(min(rendimiento_np) - 10, max(rendimiento_np) + 20)
    return fig


def graficar_boxplot_rendimiento_combustible():
    """
    Graficar un boxplot con los datos de rendimiento de combustible.
    """
    # Obtener datos de rendimiento de combustible
    rendimientos = df_vehiculos["rendimiento"]

    # Plotting
    fig = plt.figure(figsize=(8, 6))
    plt.boxplot(rendimientos, vert=False)
    plt.xlabel('Rendimiento (km/gal)')
    plt.title('Boxplot de Rendimiento de Combustible')
    plt.grid(True)

    # Añadir anotaciones
    plt.annotate(
        'Mediana', xy=(
            rendimientos.median(), 1), xytext=(
            rendimientos.median(), 1.2), arrowprops=dict(
                facecolor='black', arrowstyle='->'))
    plt.annotate(
        'Q1', xy=(
            rendimientos.quantile(0.25), 1), xytext=(
            rendimientos.quantile(0.25), 0.8), arrowprops=dict(
                facecolor='black', arrowstyle='->'))
    plt.annotate(
        'Q3', xy=(
            rendimientos.quantile(0.75), 1), xytext=(
            rendimientos.quantile(0.75), 0.8), arrowprops=dict(
                facecolor='black', arrowstyle='->'))
    plt.annotate(
        'Min', xy=(
            rendimientos.min(), 1), xytext=(
            rendimientos.min(), 1.2), arrowprops=dict(
                facecolor='black', arrowstyle='->'))
    plt.annotate(
        'Max', xy=(
            rendimientos.max(), 1), xytext=(
            rendimientos.max(), 1.2), arrowprops=dict(
                facecolor='black', arrowstyle='->'))

    # Mostrar el gráfico en Streamlit
    return fig


def graficar_scatter_rendimiento_combustible():
    """
    Graficar un scatter plot con los datos de rendimiento de combustible.
    """
    # Obtener datos de rendimiento de combustible
    vehiculos = df_vehiculos["placa"]
    vehiculos_modelo = df_vehiculos["modelo"]
    rendimientos = df_vehiculos["rendimiento"]

    # Calcular la mediana y el rango intercuartílico (IQR)
    mediana = rendimientos.median()
    q1 = rendimientos.quantile(0.25)
    q3 = rendimientos.quantile(0.75)
    iqr = q3 - q1

    # Identificar valores atípicos
    valores_atipicos = rendimientos[(
        rendimientos < q1 - 1.5 * iqr) | (rendimientos > q3 + 1.5 * iqr)]

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.scatter(vehiculos, rendimientos, color='skyblue')
    plt.xlabel('Vehículo')
    plt.ylabel('Rendimiento (km/gal)')
    plt.title('Rendimiento de Combustible por Vehículo')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)

    # Anotar la mediana
    plt.axhline(mediana, color='red', linestyle='--', label='Mediana')
    plt.annotate(f'Mediana: {mediana:.2f} km/gal',
                 xy=(1,
                     mediana),
                 xytext=(2,
                         mediana + 20),
                 arrowprops=dict(facecolor='black',
                                 arrowstyle='->'))

    # Anotar valores atípicos
    for vehiculo, rendimiento in valores_atipicos.items():
        rendimiento = round(rendimiento, 0)
        plt.annotate(f'{vehiculos_modelo[vehiculo]}: {rendimiento} km / gal',
                     xy=(vehiculo, rendimiento),
                     xytext=(-4, rendimiento * -0.25),
                     textcoords='offset points',
                     arrowprops=dict(facecolor='green', arrowstyle='->'))

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico en Streamlit
    return fig


def graficar_barras_autonomia_vehiculos():
    """
    Mostrar las estadísticas de autonomía de los vehículos.
    """
    # Encabezado principal
    st.header("Estadísticas de Autonomía de los Vehículos")

    # Calcular la autonomía de cada vehículo
    # Se multiplica la capacidad del tanque por el rendimiento del vehículo
    autonomia_np = df_vehiculos["capacidad"].to_numpy(
        dtype="float") * df_vehiculos[
            "rendimiento"].to_numpy(dtype="float")

    vehiculos = df_vehiculos["placa"]

    # Calcular y mostrar la autonomía promedio
    autonomia_promedio = round(np.mean(autonomia_np), 2)

    # Calcular y mostrar la mediana de la autonomía
    autonomia_mediana = round(np.median(autonomia_np), 2)

    # Calcular el índice del vehículo con menor autonomía
    indice_min = np.argmin(autonomia_np)

    # Calcular el índice del vehículo con mayor autonomía
    indice_max = np.argmax(autonomia_np)

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.bar(vehiculos, autonomia_np, color='skyblue')
    plt.xlabel('Vehículo')
    plt.ylabel('Autonomía (km)')
    plt.title('Autonomía de los Vehículos')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)

    # Añadir la media y la mediana como líneas horizontales
    plt.axhline(autonomia_promedio, color='red', linestyle='--',
                label=f'Media: {autonomia_promedio:.2f} km')
    plt.axhline(autonomia_mediana, color='green', linestyle='-.',
                label=f'Mediana: {autonomia_mediana:.2f} km')

    # Añadir anotaciones
    plt.annotate(f'Media: {autonomia_promedio:.2f} km',
                 xy=(10, autonomia_promedio),
                 xytext=(10, autonomia_promedio * 0.05),
                 textcoords='offset points',
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate(f'Mediana: {autonomia_mediana:.2f} km',
                 xy=(0.5, autonomia_mediana),
                 xytext=(2, autonomia_mediana * 0.05),
                 textcoords='offset points',
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate(f'Menor: {int(min(autonomia_np))} km',
                 xy=(indice_min, min(autonomia_np)),
                 xytext=(indice_min + 2, min(autonomia_np) + 3),
                 arrowprops=dict(facecolor='red', shrink=0.05))
    plt.annotate(f'Mayor: {int(max(autonomia_np))} km',
                 xy=(indice_max, max(autonomia_np)),
                 xytext=(indice_max + 2, max(autonomia_np) + 3),
                 arrowprops=dict(facecolor='green', shrink=0.05))

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico
    return fig


def graficar_boxplot_autonomia_vehiculos():
    """
    Graficar un boxplot con los datos de autonomía de los vehículos y añadir
    anotaciones.
    """
    # Calcular la autonomía de cada vehículo
    autonomia_np = df_vehiculos["capacidad"].to_numpy(
        dtype="float") * df_vehiculos["rendimiento"].to_numpy(dtype="float")

    # Calcular estadísticas de resumen
    mediana = np.median(autonomia_np)
    q1 = np.percentile(autonomia_np, 25)
    q3 = np.percentile(autonomia_np, 75)
    iqr = q3 - q1
    limites_inferiores = q1 - 1.5 * iqr
    limites_superiores = q3 + 1.5 * iqr
    valores_atipicos = autonomia_np[(autonomia_np < limites_inferiores) | (
        autonomia_np > limites_superiores)]

    # Plotting
    fig = plt.figure(figsize=(8, 6))
    plt.boxplot(autonomia_np, vert=False)

    # Añadir anotaciones
    plt.text(
        mediana,
        1,
        f'Mediana: {mediana:.2f} km',
        horizontalalignment='center',
        verticalalignment='bottom',
        color='red')
    plt.text(
        q1,
        1.1,
        f'Q1: {q1:.2f} km',
        horizontalalignment='center',
        verticalalignment='bottom',
        color='blue')
    plt.text(
        q3,
        1.1,
        f'Q3: {q3:.2f} km',
        horizontalalignment='center',
        verticalalignment='bottom',
        color='blue')

    # Añadir valores atípicos
    # Variable pos para posicionar los valores atípicos
    pos = 0
    for valor_atipico in valores_atipicos:
        plt.scatter(valor_atipico, 1,
                    color='green',
                    marker='o',
                    s=100,
                    zorder=3)
        plt.text(valor_atipico, 1.1 + pos,
                 f'Valor Atípico: {valor_atipico:.2f} km',
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='green')
        pos += 0.05

    plt.xlabel('Autonomía (km)')
    plt.title('Boxplot de Autonomía de los Vehículos')
    plt.grid(True)

    # Mostrar el gráfico
    return fig


def graficar_scatter_autonomia_vehiculos():
    """
    Graficar un scatter plot con los datos de autonomía de los vehículos
    y añadir anotaciones.
    """
    # Calcular la autonomía de cada vehículo
    autonomia = df_vehiculos["capacidad"] * df_vehiculos["rendimiento"]

    # Calcular la línea de regresión
    pendiente, intercepto, r_value, p_value, std_err = linregress(
        df_vehiculos["capacidad"], autonomia)
    # calcular los puntos de la regresión lineal
    regresion_line = intercepto + pendiente * df_vehiculos["capacidad"]

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.scatter(df_vehiculos["capacidad"], autonomia, color='skyblue')
    plt.plot(df_vehiculos["capacidad"],
             regresion_line, color='blue',
             linestyle='--',
             label=f'Regresión (R²={r_value**2:.2f})')
    plt.xlabel('Capacidad del Tanque (gal)')
    plt.ylabel('Autonomía (km)')
    plt.title('Scatter Plot de Autonomía de los Vehículos')
    plt.grid(True)

    # Anotar el rango de autonomía
    min_autonomia = np.min(autonomia)
    max_autonomia = np.max(autonomia)
    plt.axhline(min_autonomia,
                color='red',
                linestyle='-.',
                label=f'Min Autonomía: {int(min_autonomia)} km')
    plt.axhline(max_autonomia,
                color='green',
                linestyle='-.',
                label=f'Max Autonomía: {int(max_autonomia)} km')

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico
    return fig


def graficar_barras_ano_vehiculos():
    """
    Mostrar estadísticas del número de vehículos por año usando un
    gráfico de barras.
    """
    # Número de vehículos por año
    ano_vehiculos_np = df_vehiculos["año"].to_numpy()
    # Contar el numero de vehiculos por cada año
    vehiculo_ano_frecuencia = np.unique(ano_vehiculos_np,
                                        return_counts=True)

    # Calcular el promedio y la mediana
    promedio_vehiculos = np.mean(vehiculo_ano_frecuencia[1])
    mediana_vehiculos = np.median(vehiculo_ano_frecuencia[1])

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.bar(
        vehiculo_ano_frecuencia[0],
        vehiculo_ano_frecuencia[1],
        color='skyblue')
    plt.xlabel('Año')
    plt.ylabel('Número de Vehículos')
    plt.title('Número de Vehículos por Año')

    # Añadir línea para el promedio y la mediana
    plt.axhline(promedio_vehiculos, color='red', linestyle='--',
                label=f'Promedio: {promedio_vehiculos:.2f}')
    plt.axhline(
        mediana_vehiculos,
        color='green',
        linestyle='-.',
        label=f'Mediana: {mediana_vehiculos:.2f}')

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.grid(True)
    return fig


def graficar_boxplot_ano_vehiculos():
    """
    Mostrar estadísticas del estado de los vehículos usando un boxplot
    horizontal del número de vehículos por año.
    """
    # Número de vehículos por año
    ano_vehiculos_np = df_vehiculos["año"].to_numpy()
    # Contar el numero de vehiculos por cada año
    vehiculo_ano_frecuencia = np.unique(ano_vehiculos_np,
                                        return_counts=True)

    # Plotting
    fig = plt.figure(figsize=(8, 6))
    plt.boxplot(vehiculo_ano_frecuencia[1], vert=False)

# Añadir anotaciones
    plt.text(
        np.median(
            vehiculo_ano_frecuencia[1]),
        0.9,
        f'Mediana: {np.median(vehiculo_ano_frecuencia[1])}',
        horizontalalignment='center',
        verticalalignment='center',
        color='red',
        weight='bold')
    plt.text(
        np.percentile(
            vehiculo_ano_frecuencia[1],
            25),
        1.1,
        f'Cuartil 1: {np.percentile(vehiculo_ano_frecuencia[1], 25)}',
        horizontalalignment='center',
        verticalalignment='center',
        color='blue',
        weight='bold')
    plt.text(
        np.percentile(
            vehiculo_ano_frecuencia[1],
            75),
        1.1,
        f'Cuartil 3: {np.percentile(vehiculo_ano_frecuencia[1], 75)}',
        horizontalalignment='center',
        verticalalignment='center',
        color='blue',
        weight='bold')

    # Mostrar el gráfico
    plt.xlabel('Número de Vehículos por Año')
    plt.title('Boxplot del Número de Vehículos por Año')
    plt.grid(True)
    return fig


def graficar_scatter_ano_vehiculos():
    """
    Mostrar estadísticas del estado de los vehículos usando un scatter plot
    del número de vehículos por año.
    """
    # Número de vehículos por año
    ano_vehiculos_np = df_vehiculos["año"].to_numpy()
    # Contar el numero de vehiculos por cada año
    vehiculo_ano_frecuencia = np.unique(ano_vehiculos_np, return_counts=True)

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.scatter(
        vehiculo_ano_frecuencia[0],
        vehiculo_ano_frecuencia[1],
        color='skyblue')

    # Personalizar el gráfico
    plt.xlabel('Año')
    plt.ylabel('Número de Vehículos')
    plt.title('Número de Vehículos por Año')

    # Mostrar el gráfico
    plt.grid(True)
    return fig


def graficar_histograma_kilometraje_vehiculos(cortes):
    """
    Graficar un histograma del kilometraje de los vehículos.
    """
    # Datos
    kilometraje_vehiculos_np = df_vehiculos["kilometraje"].to_numpy()

    # Calcular el menor kilometraje
    kilometraje_min = np.amin(kilometraje_vehiculos_np)

    # Calcular el mayor kilometraje
    kilometraje_max = np.amax(kilometraje_vehiculos_np)

    # Calcular el kilometraje promedio
    kilometraje_promedio = round(np.mean(kilometraje_vehiculos_np), 2)

    # Calcular la mediana del kilometraje
    kilometraje_mediana = np.median(kilometraje_vehiculos_np)

    bins = cortes
    # Marcaciones eje x
    marca_eje_x = np.linspace(kilometraje_min, kilometraje_max, bins + 1)

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.hist(
        kilometraje_vehiculos_np,
        bins=bins,
        color='skyblue',
        edgecolor='black')

    # Añadir línea horizontal para promedio y mediana
    plt.axvline(
        x=kilometraje_promedio,
        color='red',
        linestyle='--',
        label=f'Promedio: {kilometraje_promedio} km')
    plt.axvline(
        x=kilometraje_mediana,
        color='green',
        linestyle='--',
        label=f'Mediana: {kilometraje_mediana} km')

    # Personalizar el gráfico
    plt.xlabel('Kilometraje (km)')
    plt.ylabel('Frecuencia')
    plt.title('Histograma del Kilometraje de los Vehículos')
    plt.legend()
    plt.xticks(marca_eje_x)

    # Mostrar el gráfico
    plt.grid(True)
    return fig


def graficar_boxplot_kilometraje_vehiculos():
    """
    Graficar un boxplot con los datos de kilometraje de los vehículos.
    """
    # Datos
    kilometraje_vehiculos_np = df_vehiculos["kilometraje"].to_numpy()

    # Calcular el kilometraje promedio
    kilometraje_promedio = round(np.mean(kilometraje_vehiculos_np), 2)

    # Calcular la mediana del kilometraje
    kilometraje_mediana = np.median(kilometraje_vehiculos_np)

    # Calcular el primer cuartil (Q1) y el tercer cuartil (Q3)
    q1 = np.percentile(kilometraje_vehiculos_np, 25)
    q3 = np.percentile(kilometraje_vehiculos_np, 75)

    # Plotting
    fig = plt.figure(figsize=(8, 6))
    plt.boxplot(kilometraje_vehiculos_np, vert=False)

    # Añadir línea para el promedio y la mediana
    plt.axvline(
        x=kilometraje_promedio,
        color='red',
        linestyle='--',
        label=f'Promedio: {kilometraje_promedio} km')
    plt.axvline(
        x=kilometraje_mediana,
        color='green',
        linestyle='--',
        label=f'Mediana: {kilometraje_mediana} km')
    plt.axvline(x=q1, color='blue', linestyle='--',
                label=f'Q1: {q1} km')
    plt.axvline(x=q3, color='orange', linestyle='--',
                label=f'Q3: {q3} km')

    # Personalizar el gráfico
    plt.xlabel('Kilometraje (km)')
    plt.title('Boxplot del Kilometraje de los Vehículos')
    plt.legend()

    # Mostrar el gráfico
    plt.grid(True)
    return fig


def graficar_barras_kilometros_ano():
    """
    Graficar un gráfico de barras de los kilómetros recorridos por año.
    """
    # Datos
    ano_vehiculos_np = (df_vehiculos["año"].to_numpy() - 2024) * -1

    # Obtener el kilometraje de todos los vehículos
    kilometraje_vehiculos_np = df_vehiculos["kilometraje"].to_numpy()

    # Calcular los kilómetros recorridos por año
    kilometros_ano_vehiculos_np = (kilometraje_vehiculos_np
                                   / ano_vehiculos_np)

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.bar(ano_vehiculos_np, kilometros_ano_vehiculos_np,
            color='skyblue')

    # Personalizar el gráfico
    plt.xlabel('Años de antigüedad de los vehículos')
    plt.ylabel('Kilómetros recorridos por los vehículos')
    plt.title('Kilómetros Recorridos por Año')
    plt.grid(axis='y')

    # Mostrar el gráfico
    return fig


def graficar_histograma_kilometros_ano(cortes):
    """
    Graficar un histograma de los kilómetros recorridos por año.
    """
    # Datos
    ano_vehiculos_np = (df_vehiculos["año"].to_numpy() - 2024) * -1

    # Obtener el kilometraje de todos los vehículos
    kilometraje_vehiculos_np = df_vehiculos["kilometraje"].to_numpy()

    # Calcular los kilómetros recorridos por año
    kilometros_ano_vehiculos_np = kilometraje_vehiculos_np / ano_vehiculos_np

    # Calcular el promedio de kilometraje por año
    kilometros_ano_promedio = round(np.mean(kilometros_ano_vehiculos_np), 2)

    # Calcular la mediana de los kilómetros recorridos por año
    kilometros_ano_mediana = round(np.median(kilometros_ano_vehiculos_np), 2)

    bins = cortes

    # Calcular la estadística del menor kilometraje recorrido por año
    kilometros_ano_min = np.amin(kilometros_ano_vehiculos_np)

    # Calcular la estadística del mayor kilometraje recorrido por año
    kilometros_ano_max = np.amax(kilometros_ano_vehiculos_np)

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.hist(
        kilometros_ano_vehiculos_np,
        bins=bins,
        color='skyblue',
        edgecolor='black')

    # Añadir línea para el promedio y la mediana
    plt.axvline(
        x=kilometros_ano_promedio,
        color='red',
        linestyle='--',
        label=f'Promedio: {kilometros_ano_promedio} km')
    plt.axvline(
        x=kilometros_ano_mediana,
        color='green',
        linestyle='--',
        label=f'Mediana: {kilometros_ano_mediana} km')

    # Personalizar el gráfico
    plt.xlabel('Kilómetros Recorridos por Año')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Kilómetros Recorridos por Año')
    plt.grid(axis='y')
    plt.xticks(np.linspace(kilometros_ano_min, kilometros_ano_max, bins + 1))
    plt.legend()

    # Mostrar el gráfico
    return fig


def graficar_scatter_kilometros_ano():
    """
    Graficar un gráfico de dispersión de los kilómetros recorridos por año.
    """
    # Datos
    ano_vehiculos_np = (df_vehiculos["año"].to_numpy() - 2024) * -1

    # Obtener el kilometraje de todos los vehículos
    kilometraje_vehiculos_np = df_vehiculos["kilometraje"].to_numpy()

    # Calcular los kilómetros recorridos por año
    kilometros_ano_vehiculos_np = kilometraje_vehiculos_np / ano_vehiculos_np

    # Calcular el promedio de kilometraje por año
    kilometros_ano_promedio = round(np.mean(kilometros_ano_vehiculos_np), 2)

    # Calcular la mediana de los kilómetros recorridos por año
    kilometros_ano_mediana = round(np.median(kilometros_ano_vehiculos_np), 2)

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.scatter(ano_vehiculos_np, kilometros_ano_vehiculos_np, color='skyblue')

    # Añadir línea horizontal para el promedio
    plt.axhline(
        y=kilometros_ano_promedio,
        color='green',
        linestyle='--',
        label=f'Kilómetros Promedio: {kilometros_ano_promedio} km')
    plt.axhline(y=kilometros_ano_mediana, color='red', linestyle='--',
                label=f'Kilómetros Mediana: {kilometros_ano_mediana} km')

    # Personalizar el gráfico
    plt.xlabel('Año del Vehículo')
    plt.ylabel('Kilómetros Recorridos por Año')
    plt.title('Gráfico de Dispersión de Kilómetros Recorridos por Año')
    plt.grid()
    plt.legend()

    # Mostrar el gráfico
    return fig


def graficar_boxplot_kilometros_ano():
    """
    Graficar un boxplot de los kilómetros recorridos por año.
    """
    # Datos
    ano_vehiculos_np = (df_vehiculos["año"].to_numpy() - 2024) * -1

    # Obtener el kilometraje de todos los vehículos
    kilometraje_vehiculos_np = df_vehiculos["kilometraje"].to_numpy()

    # Calcular los kilómetros recorridos por año
    kilometros_ano_vehiculos_np = kilometraje_vehiculos_np / ano_vehiculos_np

    # Plotting
    fig = plt.figure(figsize=(10, 6))
    plt.boxplot(kilometros_ano_vehiculos_np)

    # Añadir anotaciones
    quartiles = np.percentile(kilometros_ano_vehiculos_np, [25, 50, 75])
    plt.text(
        1,
        quartiles[0],
        f'Q1: {quartiles[0]} km',
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=10)
    plt.text(
        1,
        quartiles[1],
        f'Mediana: {quartiles[1]} km',
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=10)
    plt.text(
        1,
        quartiles[2],
        f'Q3: {quartiles[2]} km',
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=10)

    # Personalizar el gráfico
    plt.xlabel('Kilómetros Recorridos por Año')
    plt.title('Boxplot de Kilómetros Recorridos por Año')
    plt.grid(axis='y')

    # Mostrar el gráfico
    return fig


def graficar_pastel_pedidos_dia():
    """
    Graficar un gráfico de pastel para mostrar la proporción de pedidos
    por día de la semana.

    Args:
    - None

    Returns:
fig =     Figure: Objeto de matplotlib que representa el gráfico de pastel.
    """
    # Datos
    # Dividir la columna 'fecha' en fecha y hora
    df_fecha_hora = df_pedidos["fecha"].str.split(" ", expand=True)

    # Obtener el nombre del día de la semana para cada pedido
    dia_semana_pedido_np = pd.to_datetime(
        df_fecha_hora[0]).dt.day_name().to_numpy()

    # Calcular la frecuencia de pedidos para cada día de la semana
    dia_semana_ingles, frecuencia_dia_semana = np.unique(
        dia_semana_pedido_np, return_counts=True
    )

    # Diccionario con los nombres de los días de la semana
    dia_semana_espanol = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }
    # Traducir el array de nombres de días a español
    dia_semana = []
    for dia in dia_semana_ingles:
        dia_semana.append(dia_semana_espanol[dia])

    # Crear un diccionario para mapear los nombres de los días a su frecuencia
    frecuencia_por_dia = dict(zip(dia_semana, frecuencia_dia_semana))

    # Obtener los nombres de los días de la semana y sus frecuencias
    dias_semana = list(frecuencia_por_dia.keys())
    frecuencias = list(frecuencia_por_dia.values())

    # Plotting
    fig = fig = plt.figure(figsize=(8, 8))
    plt.pie(frecuencias, labels=dias_semana, autopct='%1.1f%%',
            startangle=140)
    plt.title('Proporción de Pedidos por Día de la Semana')

    # Retornar el gráfico
    return fig


def graficar_histograma_pedidos_por_hora():
    """
    Graficar un histograma de la frecuencia de pedidos por hora.

    Args:
    - None

    Returns:
    El grafico de barras de la frecuencia de pedidos por hora.
    """
    # Datos
    # Dividir la columna 'fecha' en fecha y hora
    df_fecha_hora = df_pedidos["fecha"].str.split(" ", expand=True)

    # Definir los rangos de hora
    df_rango_hora = pd.Series(
        pd.date_range("00:00", "23:59", freq="2h")
    ).dt.hour.to_numpy()
    df_rango_hora = np.append(df_rango_hora, 24)

    # Marcas para los rangos de horas del eje x
    marca_horas = []
    for i in range(0, 24, 2):
        hora_inicio = f"{i:02d}:00"
        hora_fin = f"{(i + 2) % 24:02d}:00"
        marca_horas.append(f"{hora_inicio}-{hora_fin}")

    # Obtener la hora de cada pedido
    hora_pedido_np = pd.Series(pd.to_datetime(
        df_fecha_hora[1])).dt.hour.to_numpy()

    # Calcular el histograma de frecuencia de pedidos por hora
    hora_pedido_histograma_np = np.histogram(
        hora_pedido_np, bins=df_rango_hora)

    # Obtener los datos del histograma
    frecuencias = hora_pedido_histograma_np[0]
    bins = hora_pedido_histograma_np[1]

    # Plotting
    fig = fig = plt.figure(figsize=(10, 6))
    plt.bar(bins[:-1],
            frecuencias,
            width=2,
            align='center',
            color='skyblue',
            edgecolor='black')

    # Personalizar el gráfico
    plt.xlabel('Horas del Día')
    plt.ylabel('Frecuencia de Pedidos')
    plt.title('Histograma de Frecuencia de Pedidos por Hora')
    plt.xticks(bins[:-1], marca_horas, rotation=45, ha='right')
    plt.grid(axis='y')

    return fig


def main():
    pass


if __name__ == "__main__":
    main()
