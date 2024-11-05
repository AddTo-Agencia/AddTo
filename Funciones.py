from features import personalidades, caracteristicas_fisicas, Eventos, generos
import spacy
import pandas as pd
from labels import carpetas,categorias,SubCarpeta,subCarpetaHombre,subCarpetaMujer
import os
from fuzzywuzzy import fuzz, process
import numpy as np
import yagmail

from vistahtml import vistaHtml

# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")

def fuzzy_match(token, choices, threshold=80):
    match, score = process.extractOne(token, choices, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else None

def extract_caracteristicas(text):
    # Procesar texto
    doc = nlp(text.lower())
    found_caracteristicas_fisicas = {}
    found_personalidades, found_eventos = [], {}
    found_categorias, found_genero = None, ""
    
    # Convertir listas a minúsculas para comparación
    caracteristicas_fisicas_lower = {k.lower(): [v.lower() for v in vs] for k, vs in caracteristicas_fisicas.items()}
    eventos_lower = [e.lower() for e in Eventos["Evento"]]
    generos_m_lower, generos_f_lower = [g.lower() for g in generos['M']], [g.lower() for g in generos['F']]
    personalidades_lower = [p.lower() for p in personalidades]

    # Fuzzy match para personalidades
    found_personalidades = [fuzzy_match(token.text.lower(), personalidades_lower) for token in doc if fuzzy_match(token.text.lower(), personalidades_lower)]
    
    # Buscar categoría
    for token in doc:
        for categoria in categorias:
            if categoria.lower() in token.text.lower():
                found_categorias = categoria
                break
        if found_categorias: break

    # Fuzzy match para características físicas
    for key, values in caracteristicas_fisicas_lower.items():
        found_caracteristicas_fisicas[key] = next((fuzzy_match(token.text.lower(), values) for token in doc if fuzzy_match(token.text.lower(), values)), 'Desconocido')
    
    # Fuzzy match para género
    for token in doc:
        if fuzzy_match(token.text.lower(), generos_m_lower):
            found_genero = "hombre"
            break
        elif fuzzy_match(token.text.lower(), generos_f_lower):
            found_genero = "mujer"
            break

    # Fuzzy match para eventos
    found_eventos = {token.text.lower(): fuzzy_match(token.text.lower(), eventos_lower) for token in doc if fuzzy_match(token.text.lower(), eventos_lower)}
    eventos_str = ', '.join(found_eventos.values()) or 'Desconocido'

    # Crear DataFrame
    df_data = {
        'Categoría': found_categorias or 'Desconocido',
        'Tono de piel': found_caracteristicas_fisicas.get('tono de piel', 'Desconocido'),
        'Forma del rostro': found_caracteristicas_fisicas.get('forma del rostro', 'Desconocido'),
        'Contextura física': found_caracteristicas_fisicas.get('contextura física', 'Desconocido'),
        'Longitud del cuello': found_caracteristicas_fisicas.get('longitud del cuello', 'Desconocido'),
        'Estatura': found_caracteristicas_fisicas.get('estatura', 'Desconocido'),
        'personalidad': ', '.join(found_personalidades) or 'Desconocido',
        'Evento': eventos_str
    }
    
    return expand_all_columns(pd.DataFrame([df_data]))





def categorize_predictions(y_pred, labels={}):
    # Invertir los diccionarios de etiquetas para obtener categoría a partir del índice
    inverse_labels_SubCarpetas = {v: k for k, v in labels.items()}

    # Variable para almacenar las subcarpetas
    Subcarpeta = []

    # Iterar sobre cada predicción
    for pred in y_pred.astype(int):
        subcarpeta_idx = np.maximum(pred, 0)

        # Obtener la subcarpeta de cada índice
        subcarpeta = inverse_labels_SubCarpetas.get(subcarpeta_idx, "Unknown")

        # Agregar la subcarpeta a la lista
        Subcarpeta.append(subcarpeta)

    # Eliminar duplicados convirtiendo la lista a un conjunto y luego de nuevo a lista
    Subcarpeta = list(set(Subcarpeta))

    print(Subcarpeta)
    return Subcarpeta


def enviar_correo(Edad, mensaje):
    import yagmail
    yag = yagmail.SMTP('odiseorincon@gmail.com', 'zwts ittk yfpm cvmi')

    mensaje_html = vistaHtml(mensaje,Edad)

    try:
        # Enviar el correo con el contenido HTML
        yag.send(to='addtoagencia@gmail.com', subject='Datos Sobre Usuario', contents=mensaje_html)
        return "Correo enviado correctamente."
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"




def get_images_from_folder(folder_path):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        image_files = []
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_path.lower().endswith(image_extensions):
                image_files.append(file_path)
        return image_files
    else:
        return []
    
    
    

def get_category_descriptions(categoria):
    # Descripciones de uso para cada categoría de joyería y relojería
    category_uses = {
        'Anillo de boda': 'Los anillos de boda son tradicionalmente usados como símbolo de compromiso y amor entre parejas. Se usan en el dedo anular de la mano izquierda en la mayoría de las culturas.',
        'Anillo de compromiso': 'Un anillo de compromiso se usa para simbolizar la intención de casarse. A menudo tiene una piedra preciosa y se usa en el dedo anular de la mano izquierda.',
        'Anillo': 'Los anillos pueden ser usados para la moda, como accesorios o para simbolizar un significado personal. Pueden usarse en cualquier dedo, dependiendo del estilo y la preferencia personal.',
        'Collar con colgante': 'Los collares con colgantes son ideales para añadir un toque de elegancia o para destacar un atuendo. Se usan comúnmente en eventos formales o para uso diario como accesorio de moda.',
        'Collar de perlas': 'Los collares de perlas son clásicos y atemporales. Son adecuados para eventos formales, bodas, cenas elegantes, y también pueden ser usados en entornos de negocios o como un accesorio de estilo diario.',
        'Gargantillas femeninas': 'Las gargantillas son perfectas para resaltar el cuello y combinar con escotes de diferentes estilos. Son populares en eventos de moda, fiestas o para añadir un toque elegante a un atuendo casual.',
        'Pulsera masculina': 'Las pulseras masculinas son usadas como accesorios de moda, pudiendo complementar atuendos casuales y formales. Son ideales para expresar personalidad y estilo.',
        'Reloj masculino': 'Los relojes masculinos son prácticos y elegantes, usados tanto para ver la hora como para complementar un atuendo. Son adecuados para el uso diario, en el trabajo, eventos formales y casuales.'
    }

    # Obtener la descripción para la categoría o devolver un mensaje si no está disponible
    return category_uses.get(categoria, 'Descripción no disponible')




def split_column_and_expand(df, column_to_split):
    """
    Divide una columna de un DataFrame en múltiples filas y expande las otras columnas.

    Args:
        df: El DataFrame de entrada.
        column_to_split: El nombre de la columna a dividir.

    Returns:
        Un DataFrame con la columna dividida en nuevas filas.
    """
    # Asegurar que los valores de la columna sean cadenas de texto
    df[column_to_split] = df[column_to_split].astype(str)

    # Convertir todos los valores de la columna a minúsculas
    df[column_to_split] = df[column_to_split].str.lower()

    # Dividir la columna en listas basadas en comas
    df[column_to_split] = df[column_to_split].str.split(',')

    # Explode la columna dividida para crear nuevas filas
    df_expanded = df.explode(column_to_split)

    # Quitar espacios adicionales al principio y al final de los valores de las columnas
    df_expanded[column_to_split] = df_expanded[column_to_split].str.strip()

    # Filtrar filas con valores vacíos o nulos en la columna especificada
    df_expanded = df_expanded[df_expanded[column_to_split].notna() & (df_expanded[column_to_split] != '')]

    return df_expanded



def expand_all_columns(df):
    """
    Expande todas las columnas de un DataFrame que contengan valores separados por comas.

    Args:
        df: El DataFrame de entrada.

    Returns:
        Un nuevo DataFrame con todas las columnas expandidas.
    """
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, str) and ',' in x).any():
            df = split_column_and_expand(df, col)

    return df