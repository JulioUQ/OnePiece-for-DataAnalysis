# **El One Piece** :)

La libreria OnePiece pretende ser un paquete de Python completo y fácil de usar diseñado para facilitar las tareas de datos comunes, incluida la limpieza, manipulación y visualización de datos. Inspirada en la legendaria serie de manga y anime, One Piece, esta libreria tiene como objetivo empoderar a los científicos, analistas y entusiastas de datos en sus viajes de exploración de datos, brindándoles herramientas y técnicas eficientes para conquistar los mares de datos.

> **Características:**

- **Limpieza de datos**: limpie y preprocese sin problemas los datos desordenados para garantizar la integridad y la coherencia de los datos. La biblioteca ofrece funciones para manejar valores faltantes, registros duplicados y formatos inconsistentes.
- **Manipulación de datos**: manipule y transforme fácilmente los datos para cumplir con los requisitos de análisis. Realice operaciones de filtrado, clasificación, agrupación, fusión y remodelación sin esfuerzo.
- **Visualización de datos**: cree diagramas y gráficos perspicaces y visualmente atractivos para obtener información más profunda sobre sus datos. La biblioteca admite varias técnicas de visualización, incluidos gráficos de barras, gráficos de líneas, gráficos de dispersión, histogramas y más.

> **Módulos clave:**

- **Limpieza**: módulo dedicado a tareas de limpieza de datos, con funciones para imputar valores faltantes, eliminar duplicados y manejar valores atípicos.
- **Manipulación**: módulo diseñado para operaciones de manipulación de datos, incluido el filtrado, la clasificación, la fusión y la transformación de estructuras de datos.
- **Visualización**: Módulo adaptado a la visualización de datos, que ofrece una amplia gama de funciones para generar representaciones visuales significativas y expresivas de sus datos.

## **Monkey D. Luffy**

El módulo muestra el uso de las distintas funciones que contiene el script.py llamado **`'luffy'`**. Estas son:
|**Funciones**|**Descripción**|
|:---:|---|
|import_df()   | Cargar datos desde un archivo CSV o Excel y devolver un DataFrame de pandas|
|describe_df() | Proporciona un resumen del DataFrame, incluida la forma, los tipos de datos, las estadísticas básicas, e información sobre valores nulos|
|detect_duplicates()| Detecta los registros duplicados en un dataframe, los almacena y muestra en pantalla|
|handle_null_values()|Permite manipular valores nulos en un DataFrame de pandas|
|convert_data_types()| Realiza múltiples conversiones de tipos de datos para columnas seleccionadas en un DataFrame|
|filter_df()   | Filtre un DataFrame en función de diferentes tipos de filtros para cadenas y columnas numéricas|
|groupby_df()  | Realiza operaciones y agrupación de datos en un Dataframe|
|export_df()   | Exporte un marco de datos de pandas a formato CSV o Excel|

## **Nami**
El módulo muestra el uso de las distintas funciones que contiene el script.py llamado **`'nami'`**. Estas son:

|**Funciones**|**Descripción**|
|:---:|---|
|interactive_barplot()| Crea gráficos de barras para visualizar datos categóricos, contra numéricos para comparar valores en distintas categorías|
|interactive_pie_chart()|Crea gráficos circulares para representar las frecuencias relativas de cada categoria|
|interactive_PLplots()|Crea gráficos de lineas para explorar las tendencias de variables númericas en series temporales, comparando las tendencias en distintas categorías|
|haversine_distance()|Calcular la distancia haverseno entre dos puntos de la superficie terrestre|
|add_distance_between_points()|Agregue una nueva columna 'Distance_km' al DataFrame que contiene la distancia haversine entre puntos consecutivos en función de su latitud y longitud|
|fao_map()| Crea un mapa de visualización de datos geoespaciales que incluye las geometrías de la capa FAO y marcadores opcionales|
|create_heatmap()|Crea un mapa de calor basado en columnas de latitud y longitud en el DataFrame|
|trajectory_map()|Crea un mapa de trayectoria temporal para un barco con flechas de rumbo (opcional)|
|generate_popup_content()| Genera el contenido HTML para el popup del marcador con la información del DataFrame para un punto|
