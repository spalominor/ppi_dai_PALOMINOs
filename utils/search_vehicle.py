"""
Módulo que contiene la clase VehicleSearcher para buscar vehículos en el 
dataset. 

Clases:
    VehicleSearcher: Clase para buscar vehículos en el dataset utilizando 
        criterios de búsqueda especificados en un diccionario.

Funciones:
    No hay funciones en este módulo.
    
Dependencias:
    - pandas
    - numpy
    - QueryDict from Django
"""
from django.http import QueryDict
import numpy as np
import pandas as pd



class VehicleSearcher:
    """
    Clase para buscar vehículos en el dataset utilizando criterios de búsqueda 
    especificados en un diccionario.
    
    Atributos:
        WEIGHTS (dict): Un diccionario que contiene los pesos para cada 
            criterio de búsqueda.
        vehicles (pd.DataFrame): Un DataFrame de Pandas que contiene 
            el dataset de vehículos.
        
    Métodos:
        __init__(csv_url): Inicializa la instancia de VehicleSearcher cargando 
            el dataset de vehículos.
        _prepare_data(): Convierte las columnas del DataFrame a los tipos de 
            datos correctos.
        _calculate_score(row, query): Calcula la puntuación de una fila en 
            función de los criterios de búsqueda.
        search(query): Busca vehículos en el dataset utilizando los criterios 
            de búsqueda especificados en el diccionario de consulta.
    """
    
    # Definir los pesos para cada criterio de búsqueda
    WEIGHTS = {
        'brand': 3,
        'sub_brand': 4,
        'version': 1,
        'model_year': 3
    }
    
    # Definir la URL del archivo CSV con el dataset de vehículos
    CSV_URL = 'https://raw.githubusercontent.com/spalominor/programacionparaingenieria/main/Consumo%20Gasolina%20Automoviles.csv'


    def __init__(self):
        """
        Inicializa la instancia de VehicleSearcher cargando el dataset de 
        vehículos.
        
        Args:
            csv_url (str): URL del archivo CSV con el dataset de vehículos.
            
        Returns:
            None
        """
        self.vehicles = pd.read_csv(self.CSV_URL, decimal=',')
        self._prepare_data()

    def _prepare_data(self):
        """Convierte las columnas del DataFrame a los tipos de datos 
        correctos.
        
        Args:
            Self
            
        Returns:
            None
        """
        # Cambiar el punto decimal por punto en todas las columnas
        #self.vehicles = self.vehicles.replace(',', '.', regex=True)
        
        # Convertir las columnas a los tipos de datos correctos
        self.vehicles['modelo'] = self.vehicles['modelo'].astype(int)
        self.vehicles['marca'] = self.vehicles['marca'].astype(str)
        self.vehicles['submarca'] = self.vehicles['submarca'].astype(str)
        self.vehicles['version'] = self.vehicles['version'].astype(str)
        
    def _null_query(self, query: dict) -> bool:
        """
        Comprueba si la consulta es nula o tiene valores nulos o vacíos.
        
        Args:
            query (dict): Un diccionario que contiene los criterios 
            de búsqueda.
            
        Returns:
            bool: True si la consulta es nula o tiene todos los valores nulos
            o vacíos, False en caso contrario.
        """
        if query is None:
            return True
        elif query == {}:
            return True
        elif query['brand'] == '':
            if query['sub_brand'] == '':
                if query['version'] == '':
                    if query['model_year'] is None:
                        return True
        else:
            return False
        
    def _querydict_to_dict(self, query: QueryDict) -> dict:
        """
        Convierte un objeto QueryDict en un diccionario.
        
        Args:
            query (QueryDict): Un objeto QueryDict que contiene los criterios 
            de búsqueda.
            
        Returns:
            dict: Un diccionario que contiene los criterios de búsqueda.
        """
        # Inicializar el diccionario resultante
        result = {
            'brand': '',
            'sub_brand': '',
            'model_year': None,
            'version': ''
        }
                
        # Extraer los valores de las listas
        for key in result.keys():
            if key == 'model_year':
                result[key] = query.get(f'form-{key}', [None]) or None
            else:
                result[key] = query.get(f'form-{key}', ['']) or ''
        
        return result

    def _calculate_score_vectorized(self, 
                                    vehicles: pd.DataFrame, 
                                    query: dict) -> np.ndarray:
        """
        Calcula la puntuación de cada fila en función de los criterios de 
        búsqueda utilizando un enfoque vectorizado.
        
        Args:
            vehicles (pd.DataFrame): DataFrame de vehículos.
            query (dict): Un diccionario que contiene los criterios de 
            búsqueda.
            
        Returns:
            np.ndarray: Un array numpy que contiene la puntuación de 
            cada fila.
        """
        # Inicializar el vector de puntuaciones
        scores = np.zeros(len(vehicles))
        
        # Calcular la puntuación para cada criterio de búsqueda
        if 'brand' in query:
            scores += np.where(
                vehicles['marca'].str.contains(
                    query['brand'], case=False), 
                self.WEIGHTS.get('brand', 0), 0)
        if 'sub_brand' in query:
            scores += np.where(
                vehicles['submarca'].str.contains(
                    query['sub_brand'], case=False), 
                self.WEIGHTS.get('sub_brand', 0), 0)
        if 'version' in query:
            scores += np.where(
                vehicles['version'].str.contains(
                    query['version'], case=False), 
                self.WEIGHTS.get('version', 0), 0)
        if 'model_year' in query:
            scores += np.where(
                vehicles['modelo'] == query['model_year'],
                self.WEIGHTS.get('model_year', 0), 0)
        return scores
    
    def search(self, query: dict) -> pd.DataFrame:
        """
        Busca vehículos en el dataset utilizando los criterios de búsqueda 
        especificados en el diccionario de consulta.
        
        Args:
            query (dict): Un diccionario que contiene los criterios de búsqueda.
            
        Returns:
            pd.DataFrame: Un DataFrame de Pandas que contiene los resultados de 
            la búsqueda.
        """
        # Convertir el QueryDict a un diccionario si es necesario
        if isinstance(query, QueryDict):
            query = self._querydict_to_dict(query)
            
        print(query)
        # Copiar el DataFrame de vehículos
        vehicles = self.vehicles

        # Verificar si la consulta es nula o tiene valores nulos o vacíos
        if self._null_query(query):
            # Ordenar los vehículos por su rendimiento en ciudad
            result = vehicles.sort_values(
                by='rendimiento_ciudad', ascending=True).iloc[:20]
            
            # Asignar un ID único a cada vehículo
            result['id'] = range(len(result))
            return result
        
        # Filtrar los vehículos según los criterios de búsqueda
        if query['brand'] is not None:
            vehicles = vehicles[
                vehicles['marca'].str.contains(query['brand'], 
                                               case=False)]
        if query['sub_brand'] is not None:
            vehicles = vehicles[
                vehicles['submarca'].str.contains(query['sub_brand'], 
                                                  case=False)]
        if query['version'] is not None:
            vehicles = vehicles[
                vehicles['version'].str.contains(query['version'], 
                                                 case=False)]
        if query['model_year'] is not None:
            print("model year actived")
            vehicles = vehicles[vehicles['modelo'] == query['model_year']]
        
        # Calcular la puntuación de los vehículos seleccionados
        scores = self._calculate_score_vectorized(vehicles, query)
        
        # Asignar la puntuación a los vehículos
        vehicles['score'] = scores

        # Eliminar vehículos con puntuación cero
        vehicles = vehicles[scores > 0]
        
        # Ordenar los vehículos por puntuación en orden de mayor a menor
        result = vehicles.sort_values(
            by=['score', 'rendimiento_ciudad'], ascending=False).iloc[:20]
        
        # Asignar un ID único a cada vehículo
        result['id'] = range(len(result))
        
        return result