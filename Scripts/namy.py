import folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from branca.colormap import LinearColormap
from IPython.display import display, HTML

def interactive_barplot(df, x_axis, y_axis, category_column=None, custom_title=None):
    """
    Crea múltiples gráficos de barras interactivos usando Plotly para diferentes categorías.

    parámetros:
        df (pandas.DataFrame): el DataFrame que contiene los datos.
        x_axis (str): el nombre de la columna que se usará para el eje x.
        y_axis (str): el nombre de la columna que se usará para el eje y.
        category_column (str): El nombre de la columna que representa las diferentes categorías.
        custom_title (str): Título personalizado opcional para la gráfica.

    Devoluciones:
        Ninguno (muestra la trama)
    """
    
    try:
        if category_column is None:
            categories = ['']
            fig = go.Figure(go.Bar(x=df[x_axis], y=df[y_axis]))
        else:
            categories = df[category_column].unique()
            fig = make_subplots(rows=len(categories), cols=1, shared_xaxes=True, subplot_titles=[f"{y_axis} por {x_axis} - {category}" for category in categories])
    
            for i, category in enumerate(categories, 1):
                category_df = df[df[category_column] == category]
                trace = go.Bar(x=category_df[x_axis], y=category_df[y_axis], name=category)
                fig.add_trace(trace, row=i, col=1)
    
            fig.update_layout(showlegend=len(categories) > 1)
            
        title = custom_title or f"{y_axis} por {x_axis}"
        
        fig.update_layout(height=300 * len(categories), title_text=title, title_font=dict(family='bold', size=20))
        fig.update_xaxes(title_text=x_axis, title_font=dict(family='bold', size=16), title_standoff=10)
        fig.update_yaxes(title_text=y_axis, title_font=dict(family='bold', size=16), title_standoff=10)

        fig.show()

    except Exception as e:
        print("Ocurrió un error:", e)

def interactive_pie_chart(df, column_name, category_column=None, title=None):
    """
     Cree gráficos circulares para visualizar la distribución de valores en una columna categórica para diferentes categorías.
     parámetros:

         df (pandas.DataFrame): el DataFrame que contiene los datos.
         column_name (str): el nombre de la columna categórica para la que se creará el gráfico circular.
         category_column (str, opcional): el nombre de la columna que representa las diferentes categorías. El valor predeterminado es Ninguno.
         title (str, opcional): el título de los gráficos circulares. El valor predeterminado es Ninguno.

     Devoluciones:
         Ninguno (muestra los gráficos circulares)
     """
    try:
        if column_name not in df.columns:
            raise ValueError(f"Columna '{column_name}' no encontrada en el DataFrame.")
        
        if category_column is None:
            # Cree un único gráfico circular si no se proporciona categoría_columna
            pie_chart_data = df[column_name].value_counts()
            fig = go.Figure(data=[go.Pie(labels=pie_chart_data.index, values=pie_chart_data.values)])
            fig.update_traces(marker=dict(colors=px.colors.qualitative.Plotly),
                              textfont=dict(size=14))
            fig.update_layout(title_text=title, title_font=dict(size=18), showlegend=True)
            fig.show()
        else:
            # Crear gráficos circulares para diferentes categorías
            categories = df[category_column].unique()

            for category in categories:
                category_df = df[df[category_column] == category]
                pie_chart_data = category_df[column_name].value_counts()

                fig = go.Figure(data=[go.Pie(labels=pie_chart_data.index, values=pie_chart_data.values)])
                fig.update_traces(marker=dict(colors=px.colors.qualitative.Plotly),
                                  textfont=dict(size=14))
                fig.update_layout(title_text=f"{title} - {category}", title_font=dict(size=18), showlegend=True)
                fig.show()

    except Exception as e:
        print("Ocurrió un error:", e)


# Proximas modificaciones: 
## Añadir opcion para múltiples variables en el eje y, para comparar tendencias en un único plot

def interactive_PLplots(df, x_column, y_column, show_lines=True, show_points=True, category_column=None, title=None):
    """
    Crea y muestra un gráfico interactivo utilizando Plotly con posibilidad de mostrar líneas y/o puntos.

    Parámetros:
    df (pandas.DataFrame): El DataFrame que contiene los datos.
    x_column (str): Nombre de la columna que se utilizará en el eje X.
    y_column (str): Nombre de la columna que se utilizará en el eje Y.
    category_column (str, opcional): Nombre de la columna que se utilizará para categorizar los datos. Si se proporciona,
    se generarán líneas y/o puntos separados para cada categoría.
    title (str, opcional): Título del gráfico.
    show_lines (bool, opcional): Indica si se deben mostrar líneas en el gráfico.
    show_points (bool, opcional): Indica si se deben mostrar puntos en el gráfico.

    Ejemplo de uso:
    interactive_PLplots(data, 'Tiempo', 'Valor', 'Categoría', 'Gráfico Interactivo', show_lines=True, show_points=True)
    """
    # Crea una figura vacía
    fig = go.Figure()

    # Determina el modo del trazado (líneas, puntos o ambos)
    mode = 'lines+markers' if show_lines and show_points else ('lines' if show_lines else 'markers')

    if category_column is None:
        # Agrega un trazado sin categorías
        fig.add_trace(go.Scatter(x=df[x_column], y=df[y_column], mode=mode))
    else:
        # Agrega trazados para cada categoría
        for category in df[category_column].unique():
            category_data = df[df[category_column] == category]
            fig.add_trace(go.Scatter(x=category_data[x_column], y=category_data[y_column], mode=mode, name=str(category)))

    # Actualiza el título y etiquetas de los ejes
    fig.update_yaxes(title_text=y_column)
    fig.update_layout(title_text=title)
    fig.update_xaxes(title_text=x_column, tickmode='array', tickvals=df[x_column].tolist(), ticktext=df[x_column].tolist())

    # Actualiza el estilo de las etiquetas del eje X
    fig.update_xaxes(title_font=dict(family='bold', size=16, color='black'))

    # Muestra el gráfico interactivo
    fig.show()

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcular la distancia haverseno entre dos puntos de la superficie terrestre.

    Parámetros:
         lat1, lon1: Latitud y longitud del primer punto en grados.
         lat2, lon2: Latitud y longitud del segundo punto en grados.

    Devoluciones:
         La distancia entre los dos puntos en kilómetros.
    """
    # Convertir grados a radianes
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    # Fórmula Haversine
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    earth_radius_km = 6371.0
    distance_km = earth_radius_km * c

    return distance_km

def add_distance_between_points(df):
    """
    Agregue una nueva columna 'Distance_km' al DataFrame que contiene la distancia haversine
     entre puntos consecutivos en función de su latitud y longitud.

    Parámetros:
         df: DataFrame con columnas 'Latitud' y 'Longitud'.

    Devoluciones:
         DataFrame con la nueva columna 'Distance_km' agregada.
    """
    if len(df) < 2:
        df['Distance_km'] = 0.0
        return df

    df['Prev_Latitud'] = df['Latitud'].shift(1)
    df['Prev_Longitud'] = df['Longitud'].shift(1)

    df['Distance_km'] = df.apply(
        lambda row: haversine_distance(row['Prev_Latitud'], row['Prev_Longitud'], row['Latitud'], row['Longitud']),
        axis=1
    )

    df.drop(['Prev_Latitud', 'Prev_Longitud'], axis=1, inplace=True)
    df.at[df.index[0], 'Distance_km'] = 0.0  # Establezca la distancia para la primera fila en 0.0

    return df

def fao_map(markers_df=None, lat_col='Latitud', lon_col='Longitud'):
    """
    Crea un mapa de visualización de datos geoespaciales que incluye las geometrías de la capa FAO y marcadores opcionales.

    Parámetros:
        markers_df (pandas.DataFrame, opcional): DataFrame que contiene los marcadores a agregar al mapa.
        lat_col (str, opcional): Nombre de la columna que contiene las latitudes en markers_df.
        lon_col (str, opcional): Nombre de la columna que contiene las longitudes en markers_df.

    Devoluciones:
        folium.Map: Objeto del mapa de Folium con las geometrías de la capa FAO y los marcadores.
    """
    # Leer el DataFrame 'fao' desde el archivo shapefile
    path_fao = r"P:\Proyectos\CALCULO_CIERRES\Capas GIS\monocapa_fao.shp"
    fao = gpd.read_file(path_fao)

    # Crear un mapa de Folium centrado en la latitud y longitud promedio de las geometrías
    map_center = [fao['geometry'].centroid.y.mean(), fao['geometry'].centroid.x.mean()]
    m = folium.Map(location=map_center)

    # Agregar las geometrías al mapa con etiquetas
    for idx, row in fao.iterrows():
        codigo = row['Codigo']
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x: {'color': 'black', 'fillOpacity': 0, 'fillColor': 'black'}  # Mostrar solo el contorno
        ).add_child(folium.Popup(f"Codigo: {codigo}")).add_to(m)

        # Agregar un marcador con etiqueta en el centroide de la geometría
        folium.Marker(
            location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
            icon=folium.DivIcon(html=f'<div style="font-weight: bold;">{codigo}</div>'),
            tooltip=f"Codigo: {codigo}"
        ).add_to(m)

    if markers_df is not None:
        # Agregar marcadores para los puntos con información de latitud y longitud desde 'markers_df'
        for idx, marker_row in markers_df.iterrows():
            lat = marker_row[lat_col]
            lon = marker_row[lon_col]
            # Generar el contenido del popup utilizando la función generate_popup_content
            popup_content = generate_popup_content(marker_row)
            folium.CircleMarker(
                location=[lat, lon],
                radius=2,
                popup=folium.Popup(popup_content, max_width=300),  # Usar el contenido generado como el popup
                color='blue',
                fill=True,
                fill_opacity=1
            ).add_to(m)

    # Ajustar el zoom al máximo posible
    m.fit_bounds(m.get_bounds())

    # Mostrar el mapa
    return m


def create_heatmap(df, latitude_column, longitude_column, radius=15, blur=25):
    """
    Crea un mapa de calor basado en columnas de latitud y longitud en el DataFrame.

    Parámetros:
        df: DataFrame con columnas que contienen valores de latitud y longitud.
        columna_latitud: Nombre de la columna que contiene valores de latitud.
        columna_longitud: Nombre de la columna que contiene valores de longitud.
        radio: Radio de los puntos del mapa de calor (por defecto es 15).
        difuminado: Radio de difuminado de la capa del mapa de calor (por defecto es 25).

    Devuelve:
        Objeto de mapa de Folium con la superposición del mapa de calor.
    """
    # Obtener valores de latitud y longitud del DataFrame
    latitude_values = df[latitude_column].tolist()
    longitude_values = df[longitude_column].tolist()

    # Combinar latitud y longitud en una lista de coordenadas
    locations = list(zip(latitude_values, longitude_values))

     # Calcular el centro del mapa en función del promedio de las coordenadas proporcionadas
    map_center = [sum(latitude_values) / len(latitude_values), sum(longitude_values) / len(longitude_values)]
    m = folium.Map(location=map_center, zoom_start=10)

    # Agregar la capa de mapa de calor al mapa utilizando las coordenadas, radio y difuminado proporcionados
    HeatMap(locations, radius=radius, blur=blur).add_to(m)

   # Crear una leyenda y mostrarla en el mapa
    gradient = {0.4: 'blue', 0.6: 'lime', 0.7: 'orange', 1.0: 'red'}
    legend_title = 'Density'

    gradient_legend = """
        <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: 120px; border:2px solid grey; z-index:9999; font-size:14px; background-color:rgba(255, 255, 255, 0.8);">
            <span style="display: block; text-align: center; font-weight: bold; padding-top: 5px;">{}</span>
            <span style="display: inline-block; width: 20px; height: 20px; background-color: {}; vertical-align: middle; margin-left: 5px;"></span> {}<br>
            <span style="display: inline-block; width: 20px; height: 20px; background-color: {}; vertical-align: middle; margin-left: 5px;"></span> {}<br>
            <span style="display: inline-block; width: 20px; height: 20px; background-color: {}; vertical-align: middle; margin-left: 5px;"></span> {}<br>
            <span style="display: inline-block; width: 20px; height: 20px; background-color: {}; vertical-align: middle; margin-left: 5px;"></span> {}
        </div>
    """.format(legend_title,
               gradient[0.4], '40%',
               gradient[0.6], '60%',
               gradient[0.7], '70%',
               gradient[1.0], '100%')

    m.get_root().html.add_child(folium.Element(gradient_legend))

    m.fit_bounds(m.get_bounds())

    return m

def trajectory_map(ship_data, latitud_col, longitud_col, rumbo_col=None, sort_column=None, fao_path=r"P:\Proyectos\CALCULO_CIERRES\Capas GIS\monocapa_fao.shp"):
    """
    Crea un mapa de trayectoria temporal para un barco con flechas de rumbo (opcional).

    Parámetros:
        ship_data (pandas.DataFrame): El DataFrame con los datos del barco.
        latitud_col (str): El nombre de la columna que contiene las latitudes.
        longitud_col (str): El nombre de la columna que contiene las longitudes.
        rumbo_col (str, opcional): El nombre de la columna que contiene los valores de rumbo.
        sort_column (str, opcional): El nombre de la columna para ordenar el DataFrame.
        fao_path (str, opcional): La ruta al archivo shapefile de la capa FAO.

    Devoluciones:
        Folium map object con la trayectoria temporal del barco con flechas de rumbo (opcional)
        y capa de geometrías FAO (opcional).
    """
    # Convertir las columnas de latitud y longitud a flotante
    ship_data[latitud_col] = ship_data[latitud_col].astype(float)
    ship_data[longitud_col] = ship_data[longitud_col].astype(float)
    
    # Convertir la columna de rumbo a flotante si se proporciona
    if rumbo_col:
        ship_data[rumbo_col] = ship_data[rumbo_col].astype(float)

    # Ordenar el DataFrame si se proporciona una columna para ordenar
    if sort_column:
        ship_data.sort_values(by=[sort_column], inplace=True)

    # Crear el mapa centrado en el primer punto
    map_center = [ship_data[latitud_col].iloc[0], ship_data[longitud_col].iloc[0]]
    m = folium.Map(location=map_center, zoom_start=6)

    # Agregar la capa FAO si se proporciona la ruta al shapefile
    if fao_path:
        fao = gpd.read_file(fao_path)
        for idx, row in fao.iterrows():
            codigo = row['Codigo']
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x: {'color': 'black', 'fillOpacity': 0, 'fillColor': 'black'}
            ).add_child(folium.Popup(f"Codigo: {codigo}")).add_to(m)

    # Crear una lista de coordenadas y valores para los puntos de trayectoria
    trajectory = ship_data[[latitud_col, longitud_col]].values.tolist()

    # Crear la línea de trayectoria en el mapa
    folium.PolyLine(locations=trajectory, color='blue', weight=2).add_to(m)

    # Crear flechas de rumbo y agregarlas al mapa si se proporciona la columna de rumbo
    if rumbo_col:
        for index, point in enumerate(trajectory):
            lat, lon = point
            rumbo = ship_data[rumbo_col].iloc[index]
            
            popup_content = generate_popup_content(ship_data.iloc[index])
            
            folium.Marker(
                location=(lat, lon),
                icon=folium.DivIcon(
                    icon_size=(20, 20),
                    icon_anchor=(10, 10),
                    html=f'<div style="transform: rotate({rumbo}deg); font-size: 20px;">&#8593;</div>'
                ),
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)

    return m

def generate_popup_content(row):
    """
    Genera el contenido HTML para el popup del marcador.

    Parámetros:
        row (pandas.Series): La fila correspondiente en el DataFrame.

    Devoluciones:
        str: El contenido HTML del popup.
    """
    # Generar una tabla HTML a partir de la fila del DataFrame
    html_table = row.to_frame().to_html(header=False, classes='table table-striped')

    popup_content = f"""
        <h4>Detalles:</h4>
        {html_table}
    """

    return popup_content
