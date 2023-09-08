
import pandas as pd

########################################
#### DATOS PARA PROBAR LAS FUNCIONES####
def fides():
    """
    Devuelve un DataFrame con los datos de FIDES hasta 2022.
    """
    path = r'P:/Proyectos/CALCULO_CIERRES/CONTROL CALIDAD/1.INFORMACIÓN BÁSICA NECESARIA/ARCHIVOS FIDES/FIDES Oneshot.csv'
    fides = pd.read_csv(path)

    return fides
########################################

def get_excel_sheet_names(excel_path):
    """
    Devuelve los nombres de todas las hojas en un archivo de Excel.

    Parámetros:
         excel_path (str): la ruta del archivo de Excel.

    Resultado:
       lista: Una lista que contiene los nombres de todas las hojas en el archivo de Excel.
    """
    excel_sheet_names = pd.ExcelFile(excel_path).sheet_names
    return excel_sheet_names

def import_df(filepath, sheet_name=None, encoding='utf-8', sep=',', decimal=','):
    """
    Cargar datos desde un archivo CSV o Excel y devolver un DataFrame de pandas.

    Parámetros:
        filepath (str): Ruta del archivo CSV o Excel a cargar.
        sheet_name (str, int, list, None): Opcional. Nombre o índice de la hoja a cargar en un archivo Excel. 
                                          Si es None, se asume que es un archivo CSV.
        encoding (str, optional): Codificación para usar al leer el archivo CSV. El valor predeterminado es 'utf-8'.
        separator (str, optional): Separador para usar al leer el archivo CSV. El valor predeterminado es ','.

    Devoluciones:
        pd.DataFrame: Un DataFrame de pandas que contiene los datos del archivo.
    """
    try:
        if filepath.endswith('.csv'):
            # Cargar datos de un archivo csv
            data = pd.read_csv(filepath, encoding=encoding, sep=sep, decimal=decimal)
        elif filepath.endswith('.xls') or filepath.endswith('.xlsx'):
            # Cargar datos de un archivo Excel
            if sheet_name is None:
                # Si el nombre de la hoja no es especificada, lee la primera hoja del archivo Excel
                xls = pd.ExcelFile(filepath)
                data = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
            else:
                data = pd.read_excel(filepath, sheet_name=sheet_name)
        else:
            raise ValueError("Formato de archivo no compatible. Utilice un archivo CSV o Excel.")

        return data  # Devuelve los resultados en un DataFrame de Pandas
    except Exception as e:
        print("Error al cargar los datos:", e)
        return None

def detect_duplicates(df):
    """
    Detecte duplicados en un DataFrame y guárdelos en un nuevo DataFrame para su exploración.

     Parámetros:
         df (pd.DataFrame): el DataFrame para buscar duplicados.

     Devoluciones:
         pd.DataFrame: un nuevo DataFrame que contiene las filas duplicadas del DataFrame original.
    """
    try:
        # Encuentra los registros duplicados en el DataFrame
        duplicates_mask = df.duplicated(keep=False)

        # Crea un nuevo DataFrame conteniendo los registros duplicados
        duplicate_df = df[duplicates_mask]

        return duplicate_df

    except Exception as e:
        print("Error detectando duplicados:", e)
        return None

def describe_df(data):
    """
     Proporciona un resumen del DataFrame, incluida la forma, los tipos de datos, las estadísticas básicas,
     e información sobre valores nulos.

     Parámetros:
         data (DataFrame): el pandas DataFrame que se describirá.

     Resultado:
         DataFrame: Un DataFrame resumido que contiene la información.
     """
    summary = pd.DataFrame({
        'Column': data.columns,
        'Data Type': data.dtypes,
        'Non-null Count': data.count(),
        'Null Count': data.isnull().sum(),
        'Unique Values': data.nunique()
    }).reset_index(drop=True)

    summary['Data Type'] = summary['Data Type'].astype(str)
    summary['Shape'] = f"{data.shape[0]} rows, {data.shape[1]} columns"

    # Añadir estadísticos básicos para columnas numéricas
    numeric_cols = data.select_dtypes(include=['number']).columns
    if not numeric_cols.empty:
        numeric_stats = data[numeric_cols].describe().T[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
        summary = summary.merge(numeric_stats, left_on='Column', right_index=True, how='left')

    return summary

def unique_df(df):
    """
    Genera resúmenes de categorías para las variables categóricas de un DataFrame.

    Parámetros:
        df (pandas.DataFrame): el marco de datos del que generar los resúmenes de categorías.

    Devoluciones:
        None
    """
    try:
        # Seleccionar columnas categóricas y de objeto
        categorical_columns = df.select_dtypes(include=['category', 'object']).columns

        if len(categorical_columns) == 0:
            print("No se encontraron columnas categóricas u objeto en el DataFrame.")
            return

        # Lista para almacenar resúmenes
        summaries = []

        for column in categorical_columns:
            unique_values = df[column].unique()
            summary = f"Resumen para la columna '{column}':\n{unique_values}\n"
            summaries.append(summary)

        # Imprimir todos los resúmenes
        for summary in summaries:
            print(summary)

    except Exception as e:
        print("Ocurrió un error:", str(e))


class FillValueAlreadyExistsError(Exception):
    """
    Clase de excepción personalizada para manejar casos cuando el valor de relleno especificado ya existe en la columna.   
    """
    pass

def handle_null_values(df, column_with_null, fill_value=None):
    """
    Manejar valores nulos en una columna DataFrame y, opcionalmente, llenarlos con un valor específico.

     Parámetros:
         df (pandas.DataFrame): El DataFrame a procesar.
         column_with_null (str): el nombre de la columna en el DataFrame para comprobar si hay valores nulos.
         fill_value (objeto, opcional): El valor a usar para llenar los valores nulos. El valor predeterminado es Ninguno.

     Devoluciones:
         pandas.DataFrame o None: si fill_value es None, devuelve un DataFrame que contiene filas con valores nulos en la columna especificada.
                                   Si se proporciona fill_value, completa los valores nulos en el DataFrame y devuelve Ninguno.
     """
    try:
        # Comprobación de si existe la columna en el DataFrame
        if column_with_null not in df.columns:
            raise ValueError(f"Columna '{column_with_null}' no encontrada en el DataFrame.")

        # Filtra filas donde la columna especificada tiene valores nulos
        null_records = df[df[column_with_null].isnull()].copy()

        # Si se proporciona fill_value, verifica si ya está presente en la columna
        if fill_value is not None and fill_value in df[column_with_null].values:
            raise FillValueAlreadyExistsError(f"El valor '{fill_value}' ya existe en la columna '{column_with_null}'.")

        # Si se proporciona fill_value, y la columna aún no contiene el fill_value, rellena los valores nulos
        if fill_value is not None:
            df[column_with_null].fillna(fill_value, inplace=True)

        # Devuelve el DataFrame con valores nulos 
        return null_records

    except FillValueAlreadyExistsError as e:
        print(f"Error: {e}")
        return None

class ColumnNotFoundError(Exception):
    """
    Clase de excepción personalizada para manejar casos cuando  la columna especificada no existe en el DataFrame.   
    """
    pass

def convert_data_types(df, column_data_types):
    """
    Convierte tipos de datos de múltiples columnas en un DataFrame.

      parámetros:
          df (pandas.DataFrame): El DataFrame a modificar.
          column_data_types (dict): Un diccionario que mapea los nombres de las columnas a sus tipos de datos deseados.

      Devoluciones:
          pandas.DataFrame: el DataFrame con tipos de datos convertidos.
    """
    try:
    # Comprueba si todos los nombres de las columnas existen en el DataFrame
        for col in column_data_types.keys():
            if col not in df.columns:
                raise ColumnNotFoundError(f"La columna '{col}' no existe en el DataFrame.")
            
                # Convert 'Hora' column to 'HH:MM' format
        if 'Hora' in column_data_types:
            df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M').dt.strftime('%H:%M')

        # Convert 'Fecha' column to 'YYYY-MM-DD' format
        if 'Fecha' in column_data_types:
            df['Fecha'] = df['Fecha'].dt.strftime('%Y-%m-%d')

   
        return df.astype(column_data_types)
    except Exception as e:
        print(f"Ocurrió un error durante la conversión de datos: {e}")
        return None

def filter_df(df, filters):
    """
    Filtre un DataFrame en función de diferentes tipos de filtros para cadenas y columnas numéricas.

    Parámetros:
        df (pd.DataFrame): El DataFrame a filtrar.
        filters (dict): Un diccionario que contiene nombres de columna como claves y detalles de filtro como valores.
                        Para las columnas de cadena, los detalles del filtro deben ser una tupla (filter_type, search_string). Los tipos de filtro admitidos son: 'contains', 'start_with', 'end_with', 'not_null' y 'is_null'.
                        Para las columnas numéricas, los detalles del filtro deben ser un diccionario con tipos de filtro como claves y
                        filtrar valores como valores. Los tipos de filtro admitidos son: 'equals', 'not_equal', 'greater_than', 'less_than', 'not_null' y 'is_null'

    Devoluciones:
        pd.DataFrame: Un DataFrame filtrado basado en los filtros especificados.
    """
    try:
        filtered_df = df.copy()

        for col, filter_details in filters.items():
            if col not in filtered_df.columns:
                raise ValueError(f"Columna '{col}' no encontrada en el DataFrame.")

            col_type = filtered_df[col].dtype

            if col_type in ['object', 'string']:
                filter_type, search_string = filter_details
                if filter_type == 'contains':
                    mask = filtered_df[col].str.contains(search_string, case=False, na=False)
                elif filter_type == 'start_with':
                    mask = filtered_df[col].str.startswith(search_string, na=False)
                elif filter_type == 'end_with':
                    mask = filtered_df[col].str.endswith(search_string, na=False)
                elif filter_type == 'not_null':
                    mask = filtered_df[col].notnull()
                elif filter_type == 'is_null':
                    mask = filtered_df[col].isnull()
                else:
                    raise ValueError(f"Tipo de filtro invalido '{filter_type}' para la columna '{col}'.")
                filtered_df = filtered_df[mask]

            elif col_type in ['int64', 'float64']:
                for filter_type, filter_value in filter_details.items():
                    if filter_type == 'equals':
                        mask = filtered_df[col] == filter_value
                    elif filter_type == 'not_equal':
                        mask = filtered_df[col] != filter_value
                    elif filter_type == 'greater_than':
                        mask = filtered_df[col] > filter_value
                    elif filter_type == 'less_than':
                        mask = filtered_df[col] < filter_value
                    elif filter_type == 'not_null':
                        mask = filtered_df[col].notnull()
                    elif filter_type == 'is_null':
                        mask = filtered_df[col].isnull()
                    else:
                        raise ValueError(f"Tipo de filtro invalido '{filter_type}' para la columna '{col}'.")
                    filtered_df = filtered_df[mask]
            else:
                raise ValueError(f"Tipo de datos no admitido para la columna '{col}'.")

        return filtered_df

    except Exception as e:
        print("Error aplicando el filtro:", e)
        return None

def groupby_df(data, groupby_cols, operation_choices):
    """
    Realiza operaciones y agrupación de datos en un Dataframe.

    Parámetros:
         data (DataFrame): el pandas DataFrame que contiene los datos.
         groupby_cols (lista): una lista de nombres de columna para usar como niveles de agrupación.
         operation_choices (dict): un diccionario con nombres de columna como claves y opciones de operación como valores.

     Devoluciones:
         DataFrame: un DataFrame de pandas con los resultados agrupados y agregados, con el índice reseteado.
    Example:
        groupby_cols = ['Species', 'Location']
        operation_choices = {'Weight': ['sum', 'mean']}
        aggregated_fish_data = groupby_df(fish_data, groupby_cols, operation_choices)
    """
    try:
        # Asegurate de que todas las columnas del groupby_cols y eleccion de operaciones existen en el DataFrame
        missing_cols = [col for col in groupby_cols + list(operation_choices.keys()) if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Columnas no encontradas en el DataFrame: {', '.join(missing_cols)}")

        # Ejecuta la agrupación y las operaciones según necesidad
        grouped_data = data.groupby(groupby_cols)
        aggregated_data = grouped_data.agg(operation_choices)

        # Reseteamos el índice para convertir las columnas agrupadas en columnas comunes
        aggregated_data = aggregated_data.reset_index()

        return aggregated_data

    except Exception as e:
        print("Ocurrió un error:", e)
        return None

def export_df(df, file_path, file_type='csv', sheet_name='Sheet1', index=False, append_to_excel=False):
    """
    Exporte un marco de datos de pandas a formato CSV o Excel.

     Parámetros:
         df (pd.DataFrame): El DataFrame a exportar.
         file_path (str): la ruta del archivo donde se guardará el archivo.
         file_type (str, opcional): El tipo de archivo a exportar. Opciones: 'csv' (predeterminado) o 'excel'.
         sheet_name (str, opcional): el nombre de la hoja en el archivo de Excel. El valor predeterminado es 'Hoja1'.
         index (bool, opcional): si incluir el índice en el archivo exportado. El valor predeterminado es Falso.
         append_to_excel (bool, opcional): si se agrega el marco de datos como una nueva hoja en un archivo de Excel existente.
                                          El valor predeterminado es Falso.

     Devoluciones:
         Ninguno
    """
    try:
        if file_type == 'csv':
            df.to_csv(file_path, index=index)
            print("DataFrame exportado a CSV exitosamente.")
        elif file_type == 'excel':
            # Convert file_path to string
            file_path = str(file_path)

            if append_to_excel:
                # Check if the file exists and the file_path has a valid extension
                if file_path.endswith(('.xls', '.xlsx')):
                    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                        df.to_excel(writer, sheet_name=sheet_name, index=index)
                        writer.save()
                    print(f"DataFrame incluido como una nueva Hoja en el archivo Excel existence: {file_path}")
                else:
                    raise ValueError("Ruta de archivo no válida. La ruta del archivo debe tener una extensión '.xls' o '.xlsx'.")
            else:
                df.to_excel(file_path, sheet_name=sheet_name, index=index)
                print("DataFrame exportado a Excel con éxito.")
        else:
            raise ValueError("Tipo de archivo invalido. Las opciones son: 'csv' o 'excel'.")

    except Exception as e:
        print(f"Error al exportar DataFrame a {file_type}: {e}")




    