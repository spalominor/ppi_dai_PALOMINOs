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
    plt.figure(figsize=(10, 6))
    plt.bar(vehiculos_np, rendimiento_np, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axhline(rendimiento_promedio, color='red', linestyle='dashed', linewidth=1, label='Media')
    plt.axhline(rendimiento_mediana, color='green', linestyle='dashed', linewidth=1, label='Mediana')
    plt.title('Distribución de Rendimiento de Combustible')
    plt.xlabel('Vehículo (placa)')
    plt.ylabel('Rendimiento (km/gal)')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True)
    plt.annotate(f'Menor: {min(rendimiento_np)} km/gal', xy=(indice_min, min(rendimiento_np)),
                 xytext=(indice_min + 2, min(rendimiento_np) + 3),
                 arrowprops=dict(facecolor='red', shrink=0.05))
    plt.annotate(f'Mayor: {max(rendimiento_np)} km/gal', xy=(indice_max, max(rendimiento_np)),
                 xytext=(indice_max + 2, max(rendimiento_np) + 3),
                 arrowprops=dict(facecolor='green', shrink=0.05))
    plt.ylim(min(rendimiento_np) - 10, max(rendimiento_np) + 20)
    plt.show()
    print("Correcto")
    
    st.pyplot()
    
    
def graficar_boxplot_rendimiento_combustible():
    """
    Graficar un boxplot con los datos de rendimiento de combustible.
    """
    # Obtener datos de rendimiento de combustible
    rendimientos = df_vehiculos["rendimiento"]

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.boxplot(rendimientos, vert=False)
    plt.xlabel('Rendimiento (km/gal)')
    plt.title('Boxplot de Rendimiento de Combustible')
    plt.grid(True)

    # Añadir anotaciones
    plt.annotate('Mediana', xy=(rendimientos.median(), 1), xytext=(rendimientos.median(), 1.2),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate('Q1', xy=(rendimientos.quantile(0.25), 1), xytext=(rendimientos.quantile(0.25), 0.8),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate('Q3', xy=(rendimientos.quantile(0.75), 1), xytext=(rendimientos.quantile(0.75), 0.8),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate('Min', xy=(rendimientos.min(), 1), xytext=(rendimientos.min(), 1.2),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate('Max', xy=(rendimientos.max(), 1), xytext=(rendimientos.max(), 1.2),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    # Mostrar el gráfico en Streamlit
    plt.show()
    

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
    valores_atipicos = rendimientos[(rendimientos < q1 - 1.5 * iqr) | (rendimientos > q3 + 1.5 * iqr)]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(vehiculos, rendimientos, color='skyblue')
    plt.xlabel('Vehículo')
    plt.ylabel('Rendimiento (km/gal)')
    plt.title('Rendimiento de Combustible por Vehículo')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)

    # Anotar la mediana
    plt.axhline(mediana, color='red', linestyle='--', label='Mediana')
    plt.annotate(f'Mediana: {mediana:.2f} km/gal', xy=(1, mediana), xytext=(2, mediana + 20),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    # Anotar valores atípicos
    for vehiculo, rendimiento in valores_atipicos.items():
        plt.annotate(f'{vehiculos_modelo[vehiculo]}: {int(rendimiento)} km/gal', 
                     xy=(vehiculo, rendimiento), xytext=(-4, rendimiento*-0.25), 
                     textcoords='offset points',
                     arrowprops=dict(facecolor='green', arrowstyle='->'))

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico en Streamlit
    plt.show()
    

def graficar_barras_autonomia_vehiculos():
    """
    Mostrar las estadísticas de autonomía de los vehículos.
    """
    # Encabezado principal
    st.header("Estadísticas de Autonomía de los Vehículos")

    # Calcular la autonomía de cada vehículo
    # Se multiplica la capacidad del tanque por el rendimiento del vehículo
    autonomia_np = df_vehiculos["capacidad"].to_numpy(dtype="float") * df_vehiculos[
        "rendimiento"
    ].to_numpy(dtype="float")

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
    plt.figure(figsize=(10, 6))
    plt.bar(vehiculos, autonomia_np, color='skyblue')
    plt.xlabel('Vehículo')
    plt.ylabel('Autonomía (km)')
    plt.title('Autonomía de los Vehículos')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    
    # Añadir la media y la mediana como líneas horizontales
    plt.axhline(autonomia_promedio, color='red', linestyle='--', label=f'Media: {autonomia_promedio:.2f} km')
    plt.axhline(autonomia_mediana, color='green', linestyle='-.', label=f'Mediana: {autonomia_mediana:.2f} km')

    # Añadir anotaciones
    plt.annotate(f'Media: {autonomia_promedio:.2f} km', xy=(10, autonomia_promedio),
                 xytext=(10, autonomia_promedio*0.05), textcoords='offset points',
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate(f'Mediana: {autonomia_mediana:.2f} km', xy=(0.5, autonomia_mediana),
                 xytext=(2, autonomia_mediana*0.05), textcoords='offset points',
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.annotate(f'Menor: {int(min(autonomia_np))} km', xy=(indice_min, min(autonomia_np)),
                 xytext=(indice_min + 2, min(autonomia_np) + 3),
                 arrowprops=dict(facecolor='red', shrink=0.05))
    plt.annotate(f'Mayor: {int(max(autonomia_np))} km', xy=(indice_max, max(autonomia_np)),
                 xytext=(indice_max + 2, max(autonomia_np) + 3),
                 arrowprops=dict(facecolor='green', shrink=0.05))

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.show()
    
    st.pyplot()
    

def graficar_boxplot_autonomia_vehiculos():
    """
    Graficar un boxplot con los datos de autonomía de los vehículos y añadir anotaciones.
    """
    # Calcular la autonomía de cada vehículo
    autonomia_np = df_vehiculos["capacidad"].to_numpy(dtype="float") * df_vehiculos[
        "rendimiento"
    ].to_numpy(dtype="float")

    # Calcular estadísticas de resumen
    mediana = np.median(autonomia_np)
    q1 = np.percentile(autonomia_np, 25)
    q3 = np.percentile(autonomia_np, 75)
    iqr = q3 - q1
    limites_inferiores = q1 - 1.5 * iqr
    limites_superiores = q3 + 1.5 * iqr
    valores_atipicos = autonomia_np[(autonomia_np < limites_inferiores) | (autonomia_np > limites_superiores)]

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.boxplot(autonomia_np, vert=False)

    # Añadir anotaciones
    plt.text(mediana, 1, f'Mediana: {mediana:.2f} km', horizontalalignment='center', verticalalignment='bottom', color='red')
    plt.text(q1, 1.1, f'Q1: {q1:.2f} km', horizontalalignment='center', verticalalignment='bottom', color='blue')
    plt.text(q3, 1.1, f'Q3: {q3:.2f} km', horizontalalignment='center', verticalalignment='bottom', color='blue')

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
    plt.show()


def graficar_scatter_autonomia_vehiculos():
    """
    Graficar un scatter plot con los datos de autonomía de los vehículos y añadir anotaciones.
    """
    # Calcular la autonomía de cada vehículo
    autonomia = df_vehiculos["capacidad"] * df_vehiculos["rendimiento"]

    # Calcular la línea de regresión
    pendiente, intercepto, r_value, p_value, std_err = linregress(df_vehiculos["capacidad"], autonomia)
    # calcular los puntos de la regresión lineal
    regresion_line = intercepto + pendiente * df_vehiculos["capacidad"]

    # Plotting
    plt.figure(figsize=(10, 6))
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
    plt.show()
    
    st.pyplot()
    
def graficar_barras_ano_vehiculos():
    """
    Mostrar estadísticas del estado de los vehículos, incluyendo número de vehículos por año, kilometraje y kilómetros recorridos por año.
    """
    # Número de vehículos por año
    ano_vehiculos_np = df_vehiculos["año"].to_numpy()
    # Contar el numero de vehiculos por cada año
    vehiculo_ano_frecuencia = np.unique(ano_vehiculos_np, return_counts=True)

    # Calcular el promedio y la mediana
    promedio_vehiculos = np.mean(vehiculo_ano_frecuencia[1])
    mediana_vehiculos = np.median(vehiculo_ano_frecuencia[1])

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(vehiculo_ano_frecuencia[0], vehiculo_ano_frecuencia[1], color='skyblue')
    plt.xlabel('Año')
    plt.ylabel('Número de Vehículos')
    plt.title('Número de Vehículos por Año')

    # Añadir línea para el promedio y la mediana
    plt.axhline(promedio_vehiculos, color='red', linestyle='--', label=f'Promedio: {promedio_vehiculos:.2f}')
    plt.axhline(mediana_vehiculos, color='green', linestyle='-.', label=f'Mediana: {mediana_vehiculos:.2f}')

    # Mostrar leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.grid(True)
    plt.show()
    
    
graficar_barras_ano_vehiculos()


    

def graficos_autonomia_vehiculos():
        # Indicar la unidad de medida y explicar qué es la autonomía
    st.write("Autonomía medida en kilómetros (km)")
    st.write("""
        Distancia máxima aproximada que puede recorrer
        un vehículo con un tanque de combustible lleno.
    """)
    st.write("""
        La autonomía se calcula multiplicando la capacidad
        del tanque de combustible por el rendimiento del vehículo.
    """)
    