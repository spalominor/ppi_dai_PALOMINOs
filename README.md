# Flutas 🍇: Gestor de Flotas y Rutas Vehículares

[App Flutas](https://flutas.fly.dev)

<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/spalominor/ppi_dai_PALOMINOs?style=flat&color=green">

## Contenido
- [Descripción del Proyecto 📖](#descripción-del-proyecto-)
- [Funcionalidades 🎯](#Funcionalidades-)
- [Justificación de la Idea 💡](#justificación-de-la-idea-)
- [Librerías Utilizadas 📚](#librerías-utilizadas-)
- [Información Profesional 👨‍🎓](#información-profesional-)
- [Contacto 📲](#contacto-)

## Descripción del Proyecto 📖

Flutas App es una plataforma integral diseñada para simplificar la gestión de vehículos y rutas para los usuarios. Desde comparar el rendimiento de diferentes vehículos hasta calcular el costo de combustible para rutas específicas, Flutas App ofrece una amplia gama de funcionalidades. Además de permitir la visualización de análisis avanzados a través de gráficos y mapas interactivos, la aplicación también integra características de análisis geoespacial y clustering para proporcionar información detallada sobre el consumo de combustible y las rutas más eficientes.

## Funcionalidades 🎯

1. **Crear y Ver Vehículos**
    - Agrega y visualiza detalles de tus vehículos.
    - Incluye información como marca, modelo, año, eficiencia de combustible, tipo de combustible, etc.

2. **Comparar Vehículos**
    - Compara diferentes vehículos en función de sus especificaciones y eficiencia de combustible.

3. **Calcular Costo de Ruta**
    - Calcula el costo de una ruta específica basándote en la distancia y la eficiencia de combustible de tu vehículo.
    - Utiliza aproximaciones en base a la distancia de Manhattan para obtener la distancia entre dos ubicaciones.

4. **Ver y Administrar Rutas**
    - Registra y visualiza todas las rutas que has creado.
    - Edita y elimina rutas existentes según sea necesario.

5. **Análisis de Vehículos**
    - Analiza el rendimiento de tus vehículos y obtén información detallada sobre su uso y eficiencia.

6. **Visualización de Mapas**
    - Proporciona visualizaciones de rutas utilizando mapas de clúster y mapas de calor.
    - Ayuda a entender mejor tus patrones de viaje.

## Justificación de la Idea 💡

La **Flutas App** proporciona una solución integral para la gestión y análisis de vehículos y rutas, ofreciendo múltiples beneficios a sus usuarios:

### 1. Optimización del Costo de Combustible

Una de las principales preocupaciones de los propietarios de vehículos es el costo del combustible. Con la funcionalidad de **Calcular Costo de Ruta**, los usuarios pueden planificar sus viajes de manera más eficiente, sabiendo de antemano cuánto gastarán en combustible. Esto es particularmente útil para viajes largos o frecuentes, permitiendo a los usuarios presupuestar con precisión y encontrar rutas más económicas.

### 2. Comparación de Vehículos

La capacidad de **Comparar Vehículos** permite a los usuarios tomar decisiones informadas al comprar o utilizar diferentes vehículos. Pueden comparar especificaciones y eficiencias de combustible para elegir el vehículo más adecuado según sus necesidades, contribuyendo a una elección más económica y ecológica.

### 3. Gestión Eficiente de Vehículos

Con la funcionalidad de **Crear y Ver Vehículos**, los usuarios pueden llevar un registro detallado de todos sus vehículos en un solo lugar. Esto incluye datos importantes como la eficiencia de combustible, el tipo de combustible, y el año del modelo, lo cual es esencial para el mantenimiento y la planificación de los costos.

### 4. Análisis Detallado de Rutas y Vehículos

La sección de **Análisis de Vehículos** proporciona a los usuarios un entendimiento profundo del rendimiento de sus vehículos. Pueden identificar patrones de uso, evaluar la eficiencia a lo largo del tiempo, y hacer ajustes necesarios para mejorar el rendimiento y reducir costos.

### 5. Visualización Interactiva de Rutas

Las **Visualizaciones de Mapas** con mapas de clúster y mapas de calor permiten a los usuarios ver de manera clara y gráfica sus patrones de viaje. Esto puede ayudar a identificar rutas frecuentes, zonas de alto tráfico, y optimizar los desplazamientos diarios.

### 6. Facilidad de Uso y Accesibilidad

Con una interfaz intuitiva y fácil de usar, Flutas App hace que la gestión de vehículos y rutas sea accesible para cualquier usuario, sin necesidad de conocimientos técnicos avanzados. La integración del modo claro y oscuro mejora la experiencia del usuario al adaptarse a diferentes condiciones de iluminación.

### 7. Ahorro de Tiempo y Recursos

Al centralizar la información y proporcionar herramientas automatizadas para el cálculo de costos y análisis, la aplicación ahorra tiempo a los usuarios y reduce la necesidad de realizar cálculos manuales. Esto se traduce en una mayor eficiencia y productividad.

### Conclusión

En resumen, Flutas App es una herramienta poderosa y versátil que aborda las necesidades esenciales de los propietarios de vehículos. Al ofrecer funcionalidades que permiten la gestión eficiente, análisis detallado y visualización clara de datos, la aplicación ayuda a los usuarios a tomar decisiones informadas, optimizar sus costos y mejorar su experiencia de manejo.

## Librerías Utilizadas 📚

En la **Flutas App** hemos integrado varias librerías de Python para diferentes funcionalidades de análisis y visualización de datos. A continuación, se detalla el uso de cada una:

1. **NumPy**:  
   <img src="https://numpy.org/images/logo.svg" width="100"/>

**Numpy** se utilizó en la aplicación para:
- **Manejo de Pesos en Resultados de Búsqueda de Autos**: Numpy se emplea para asignar y manejar los pesos de los resultados de búsqueda, optimizando la relevancia de los vehículos mostrados.
- **Operaciones con Arreglos y Matrices**: Facilita las operaciones entre arreglos y matrices, permitiendo la comparación eficiente entre diferentes autos en términos de rendimiento y características.

2. **Pandas**:  
   <img src="https://pandas.pydata.org/static/img/pandas_secondary.svg" alt="Pandas" width="100"/>

**Pandas** se usó para:
- **Manejo de Búsquedas desde la Base de Datos**: Las búsquedas realizadas en la base de datos se manejan en DataFrames de Pandas, mejorando la organización y manipulación de los datos.
- **Motor de Búsqueda de Vehículos**: Pandas se emplea para manejar el motor de búsqueda de vehículos, permitiendo consultas eficientes y precisas.
- **Almacenamiento Temporal y Análisis**: Los resultados y análisis temporales se almacenan en DataFrames, facilitando la visualización y manipulación de los datos.
- **Preparación de Datos para Cálculos y Gráficas**: Los datos se organizan y preparan para realizar cálculos con Scipy y Geopandas, y para generar gráficas con Matplotlib.

3. **Matplotlib**:  
   <img src="https://icon.icepanel.io/Technology/svg/Matplotlib.svg" alt="Matplotlib" width="100"/>

**Matplotlib** se utilizó para:
- **Gráficas de Información de Vehículos**: Genera gráficos de barras y otras visualizaciones para mostrar información relevante sobre los vehículos.
- **Visualización de Mapas**: Contribuye a graficar correctamente los mapas generados con información procesada por Geopandas y Scipy.
     
4. **SciPy**:  
   <img src="https://scipy.org/images/logo.svg" alt="SciPy" width="100"/>
   
**Scipy** se utilizó para:
- **Cálculos de Clustering**: Realiza cálculos para mostrar clusters de direcciones en un mapa, identificando patrones y agrupaciones de ubicaciones.
- **Cálculos de Consumo de Combustible**: Permite calcular el consumo de combustible entre dos ubicaciones utilizando la distancia de Manhattan, integrando datos geográficos y de eficiencia de vehículos.

5. **Geopandas**:  
   <img src="https://docs.geopandas.org/en/v0.14.1/_images/geopandas_icon.png" alt="Geopandas" width="100"/>
   
**Geopandas** se usó para:
- **Decodificación de Direcciones**: Convierte direcciones en coordenadas geográficas, permitiendo calcular distancias euclidianas y otras con la ayuda de Scipy.
- **Cálculos Geográficos**: Crea índices de puntos geográficos para identificar aquellos que están cerca entre sí, mejorando la precisión de los análisis espaciales.
- **Organización para Visualización**: Prepara y organiza la información geográfica para ser graficada con Matplotlib y visualizada en mapas interactivos con Folium.

## Información Profesional 👨‍🎓

- **Nombre:** Samuel Palomino Restrepo.
- **Ubicación:** Medellín, Antioquia.
- **Información profesional:** Soy bachiller, actualmente estudiante de tercer semestre en el programa de Ingeniería de Sistemas e Informática en la Universidad Nacional - Sede Medellín. Tengo conocimientos básicos en Python, JavaScript, C# y SQL.

## Contacto 📲

[![Email](https://img.shields.io/badge/Email-spalominor%40unal.edu.co-green?style=for-the-badge&logo=gmail)](mailto:spalominor@unal.edu.co)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/samuel-palomino-9680352ba/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/spalominor)
[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white)](https://stackoverflow.com/users/23651826/spalominor)

## Hecho con 🤝
Este documento fue hecho con la ayuda de:
[![ChatGPT](https://img.shields.io/badge/ChatGPT-Informational?style=flat&logo=openai&logoColor=white)](https://openai.com/chatgpt)
[![Gemini](https://img.shields.io/badge/Gemini-Informational?style=flat&logo=google&logoColor=white)](https://gemini.google.com/app)
[![Shields.io](https://img.shields.io/badge/Shields.io-Informational?style=flat&logo=javascript&logoColor=white)](https://shields.io/)

