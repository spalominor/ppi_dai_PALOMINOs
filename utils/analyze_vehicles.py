"""
Módulo que permite analizar vehículos en función de los criterios del
dataframe.

Clases:
    VehicleAnalyzer: Clase que permite analizar vehículos en función de los 
    criterios del dataframe.
    
Funciones:
    No hay funciones en este módulo.
"""
import pandas as pd
import numpy as np



class VehicleAnalyzer:
    """
    Clase que permite analizar vehículos en función de los criterios del
    dataframe.
    
    Attributes:
        CUALITATIVAS (list): Lista de columnas cualitativas.
        CUANTITATIVAS_DISCRETAS (list): Lista de columnas cuantitativas 
            discretas.
        CUANTITATIVAS (list): Lista de columnas cuantitativas.
        PRECIO_COMBUSTIBLE (dict): Diccionario que contiene el precio del 
        combustible por tipo.
        KILOMETROS_ANUALES (int): Estimación de kilómetros recorridos 
            anualmente.
            
    Métodos:
        _differenciate(vehicles): Analiza los vehículos en función a sus 
            características.
        _anual_estimation(vehicles): Calcula las estimaciones anuales de 
            emisiones de CO2, NOx y consumo de combustible para los vehículos.
        _precio_combustible(row): Devuelve el precio del combustible según 
            el tipo.
        analyze(vehicles): Analiza de manera general vehículos en función de 
            sus características.
    """
    # Discriminar las columnas del DataFrame según su tipo
    CUALITATIVAS = ['marca', 
                    'submarca',
                     'modelo',
                     'version',
                     'transmision',
                     'combustible',
                     'categoria'
                     ]
    CUANTITATIVAS_DISCRETAS = ['cilindros',
                                'potencia',
                                'tamano',
                                'efecto_invernadero',
                                'contaminacion_aire'
                                ]
    CUANTITATIVAS = ['rendimiento_ciudad',
                    'rendimiento_carretera',
                    'rendimiento_combinado',
                    'co2',
                    'nox'
                    ]
    
    # Definir el precio del combustible según el tipo [$/L] [1gal = 3.79 L]
    # 15.000 y 10.000 pesos el galón de gasolina y diesel respectivamente
    PRECIO_COMBUSTIBLE = {'gasolina': 3950, 'diesel': 2650}
    
    # Definir la estimación de kilómetros recorridos anualmente
    KILOMETROS_ANUALES = 20000
    
    INDEX_LABELS = ['Marca',
                     'Submarca',
                     'Modelo',
                     'Versión',
                     'Transmisión',
                     'Combustible',
                     'Categoría',
                     'Cilindros',
                     'Potencia (hp)',
                     'Tamaño (L)',
                     'Calificación de efecto invernadero',
                     'Calificación de contaminación aire',
                     'Rendimiento en ciudad (km/L)',
                     'Rendimiento en carretera (km/L)',
                     'Rendimiento combinado (km/L)',
                     'Emisiones de CO2 (g/km)',
                     'Emisiones de NOx (g/km)',
                     'Emisiones de CO2 anuales (kg)',
                     'Emisiones de NOx anuales (kg)',
                     'Costo anual de combustible ($)']
        
    
    def _differenciate(self, vehicles: pd.DataFrame) -> pd.DataFrame:
        """
        Analiza los vehículos en función a sus características.
        
        Args:
            vehicles (pd.DataFrame): DataFrame de vehículos a analizar.
            
        Returns:
            pd.DataFrame: DataFrame de vehículos con una columna adicional 
            que contiene las diferencias entre cada valor y el máximo valor 
            en su respectiva columna.
        """
        # Obtener las columnas cualitativas, discretas y cuantitativas
        informacion_vehicles = vehicles[self.CUALITATIVAS]
        discretas_vehicles = vehicles[self.CUANTITATIVAS_DISCRETAS]
        valores_vehicles = vehicles[self.CUANTITATIVAS]
        
        # Convertir las columnas a tipo numérico
        discretas_vehicles = discretas_vehicles.apply(pd.to_numeric, 
                                                      errors='coerce')
        valores_vehicles = valores_vehicles.apply(pd.to_numeric, 
                                                  errors='coerce')
        
        # Obtener los valores de las columnas discretas
        np_discretas = discretas_vehicles.to_numpy()
        
        # Calcular el máximo valor de cada columna discreta
        np_max_discretas = np.max(np_discretas, axis=0)
        
        # Obtener los valores de las columnas cuantitativas
        np_valores = valores_vehicles.to_numpy()
        
        # Calcular el máximo valor de cada columna cuantitativa
        np_max_valores = np.max(np_valores, axis=0)
        
        # Calcular la diferencia entre cada valor y el máximo valor
        diferencia_discretas = np_discretas - np_max_discretas
        diferencia_valores = (
            np_valores - np_max_valores) / np_max_valores * 100
        
        # Unir los arreglos de numpy horizontalmente
        diferencia_df = pd.DataFrame(
            np.hstack((diferencia_discretas, diferencia_valores)),
            columns=self.CUANTITATIVAS_DISCRETAS + self.CUANTITATIVAS
        )
        
        # Definir una máscara para los valores 0, es decir, los valores
        # que antes eran máximos
        zero_mask = (diferencia_df == 0)
        
        # Crear un DataFrame temporal con los originales valores máximos
        max_df = pd.concat([discretas_vehicles, valores_vehicles], axis=1)
        
        print(max_df.shape)
        print(diferencia_df.shape)
        # Reemplazar los valores 0 por los máximos valores de cada columna
        diferencia_df = diferencia_df.mask(zero_mask, max_df)
        
        
        # Convertir las columnas a tipo float
        diferencia_df.astype(float)
        
        return pd.concat([informacion_vehicles, diferencia_df], axis=1)
            
    
    def _anual_estimation(self, vehicles: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula las estimaciones anuales de emisiones de CO2, NOx y consumo
        de combustible para los vehículos. Se tiene en cuenta el precio del
        combustible, el rendimiento en ciudad de los vehículos en km/L 
        y la cantidad de kilómetros recorridos anualmente (20,000 km).
        
        Args:
            vehicles (pd.DataFrame): DataFrame de vehículos.
            
        Returns:
            pd.DataFrame: DataFrame de vehículos con las estimaciones 
            anuales de emisiones de CO2, NOx y costo del consumo
            de combustible.
        """
        # Calcular el precio del combustible según el tipo
        precio_combustible = vehicles['combustible'].apply(
            self._precio_combustible)

        # Convertir a un arreglo de numpy para realizar operaciones
        np_precio_comb = precio_combustible.to_numpy()
        
        # Convertir a un arreglo de numpy para realizar operaciones
        np_rendimiento = vehicles['rendimiento_ciudad'].to_numpy()

        kilometros_anuales = self.KILOMETROS_ANUALES
        
        # [$/L] * [km/L] / [km/año] = [$/año]
        np_precio_anual = np_precio_comb * kilometros_anuales / np_rendimiento 
        
        # Convertir a un arreglo de numpy para realizar operaciones
        np_co2 = vehicles['co2'].to_numpy()
        
        # [g/km] * [km/año] = [kg/año] 
        np_co2_anual = np_co2 * self.KILOMETROS_ANUALES / 1000
        
        np_nox = vehicles['nox'].to_numpy()
        
        # [g/km] * [km/año] = [kg/año]
        np_nox_anual = np_nox * self.KILOMETROS_ANUALES / 1000
        
        # Crear un DataFrame con las estimaciones anuales
        estimaciones_df = pd.DataFrame({
            'co2_anual_kg': np_co2_anual,
            'nox_anual_kg': np_nox_anual,
            'costo_anual_combustible': np_precio_anual
        })
        
        return estimaciones_df
        
        
    def _precio_combustible(self, row: pd.Series) -> float:
        """
        Devuelve el precio del combustible según el tipo.
        
        Args:
            combustible (str): Tipo de combustible.
            
        Returns:
            float: Precio del combustible.
        """
        # Devolver el precio del combustible según el tipo
        if row == 'Gasolina':
            return self.PRECIO_COMBUSTIBLE['gasolina']
        elif row == 'Diesel':
            return self.PRECIO_COMBUSTIBLE['diesel']
        else:
            return 0
        
        
    def _clean_data(self, vehicles: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia los datos del DataFrame de vehículos.
        
        Args:
            vehicles (pd.DataFrame): DataFrame de vehículos a limpiar.
            
        Returns:
            pd.DataFrame: DataFrame de vehículos limpio.
        """
        # Eliminar filas con valores nulos
        vehicles = vehicles.dropna()
        
        # Eliminar filas con valores duplicados
        vehicles = vehicles.drop_duplicates()
        
        # Reemplaza los valores "?" con 0
        vehicles['contaminacion_aire'].str.replace('?',
         '0')
        
        return vehicles
           
    
    def analyze(self, selected_vehicles) -> pd.DataFrame:
        """
        Analiza de manera general vehículos en función de sus características.
        Cada fila representa un vehículo y cada columna una característica.
        
        Args: 
            vehicles (pd.DataFrame): DataFrame de vehículos a analizar.
            
        Returns:
            pd.DataFrame: DataFrame de vehículos con las diferencias 
            entre cada valor y el máximo valor en su respectiva columna.
            Estimaciones anuales de emisiones de CO2, NOx y costo del consumo
            de combustible.
        """
        # Convertir la lista de vehículos a un DataFrame de Pandas
        vehicles = pd.DataFrame(selected_vehicles)
        
        # Limpiar los datos del DataFrame
        vehicles = self._clean_data(vehicles)
        
        # Analizar los vehículos en función a sus características
        diferencias_df = self._differenciate(vehicles=vehicles)
        
        # Calcular las estimaciones anuales de emisiones de CO2, NOx, etc.
        estimaciones_df = self._anual_estimation(vehicles=vehicles)
        
        # Unir los DataFrames horizontalmente
        analysis_df = pd.concat([diferencias_df, estimaciones_df], axis=1)
        
        # Aproximar los valores de las columnas cuantitativas a enteros
        for column in self.CUANTITATIVAS:
            analysis_df = analysis_df.fillna(0)
            analysis_df[column] = analysis_df[column].astype(int)
            
        for column in self.CUANTITATIVAS_DISCRETAS:
            analysis_df = analysis_df.fillna(0)
            analysis_df[column] = analysis_df[column].astype(int)
            
        analysis_df[
            'costo_anual_combustible'] = analysis_df[
                'costo_anual_combustible'].astype(int)
        
        # Transponer el DataFrame para obtener 20 filas y n columnas
        # donde n es el número de vehículos
        analysis_df = analysis_df.T

        # Renombrar los índices del DataFrame
        analysis_df.rename_axis('Características', axis=1, inplace=True)
        
        # Cambiar los índices del DataFrame
        analysis_df.index = pd.Index(self.INDEX_LABELS)
        
        return analysis_df
        