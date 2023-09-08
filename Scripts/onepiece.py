
import pandas as pd
import xlwings as xw
import os
from pytube import YouTube ## For the Lattest version run --> python -m pip install git+https://github.com/pytube/pytube
import aspose.words as aw

def xlimport():
    '''Esta funcion toma toda la región actual de rango, hoja y libro de excel actuales.'''
    data = xw.books.active.app.selection.current_region.value
    df = pd.DataFrame(data[1:], columns = data[0])
    return df

def xlexport(df):
    '''Esta funcion exporta el DataFrame 'df' a la celda activa de excel'''
    xw.books.active.app.selection.options(index=False).value = df

def sheets():
    '''Esta función devuelve el nombre de la hoja activa'''
    return xw.books.active.sheets.active

def xllist():
    '''Introduce la tabla actual en una lista. La idea es coger listas para filtrar en un df.isin() de pandas'''
    data = xw.books.active.app.selection.current_region.value
    return data

def value_counts(df):
    '''Esta función utiliza la función de pandas 'value_counts' para lanzarla a un dataframe en bucle y pegarlo en excel para visualizarlo'''
    try:
        wb = xw.books.active
        aux = True

    except:
        wb = xw.Book()
        aux = False

    ws = wb.sheets.active
    rg = ws.range('A3')
    ws.range('A1').value = 'value_counts'
    fields = list(df.columns)
    for field in fields:
        #rg.offset(-1, 0).value = field
        value_counts = df[field].value_counts()
        rg.options(data_types = 'text').value = value_counts
        rg = rg.offset(0, 3) 

def mp3Download():
    '''Esta función recibe un URL de Youtube y descarga en un PATH determinado el audio del video en formato mp3'''
    # URL introducido por el usuario
    print("________Aplicación para descargar mp3__________")
    yt = YouTube(
        str(input("Introduce el URL de el video que quieras descargar el audio: \n>> ")))

    # Estraer solo el audio
    video = yt.streams.filter(only_audio=True).first()

    # Comprobar el destino donde guardar el archivo
    print("Introduce el destino de almacenamiento (dejalo en blanco para el directorio actual)")
    destination = str(input(">> ")) or '.'

    # Descargar el archivo
    out_file = video.download(output_path=destination)

    # Guardar el archivo
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    # Resultado del exito
    print(yt.title + " ha sido descargado exitosamente.")

def convertfile():
    '''Esta función recibe un archivo en cualquier tipo de formato y lo convierte otro formato deseado'''
    # Cargar un documento de cualquier formato
    print("________Aplicación para convertir archivos pdf, docx, html & jpg__________")
    doc = aw.Document(
      str(input("Introduce el PATH del archivo que desee convertir: \n>> ")))

    # Comprobar el destino donde guardar el archivo
    print("Introduce el destino de almacenamiento (dejalo en blanco para el directorio actual)")
    destination = str(input(">> ")) or '.'

    # Guarda el archivo en un formato determinado.
    doc.save(destination +
        str(input("Introduce el nuevo nombre del archivo y su extensión deseada: \n>> ")))

    # Resultado del exito
    print("Ha sido convertido exitosamente :)")

######################################
###### LOADING DATA   ################
######################################

pathC = r'C:\Users\jubeda2\Documents\Consultas jubeda2\Consulta de información SIPE\#6774 - Datos Esfuerzo Parques Eólicos\Output\Redmine 6774.xlsx'

dfC = pd.read_excel(pathC, header=0) 

# Dimensiones y tipo del set de datos
print('Tipo del set de datos: ',  type(dfC))
print('Dimensionalidad del set de datos: ', dfC.shape)
print('Estadísticos básicos: \n', (dfC.describe()))
print('Valores nulos: \n', (dfC.isnull().sum()))

# Comprobación del correcto cargado el dataframe spark, mostrando los 10 primeros registros
dfC.head(n=10)



##Plotly: Plotly is a Python library that provides interactive data visualization capabilities. With Plotly, you can connect to your SQL 
##database using libraries like Pandas, retrieve the data, and create interactive charts, graphs, and dashboards. Plotly supports various 
##chart types and can be integrated with web applications or Jupyter notebooks.

