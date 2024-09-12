from features import personalidades, caracteristicas_fisicas, Eventos, generos
import spacy
import pandas as pd
from labels import carpetas,categorias,SubCarpeta
import os
from fuzzywuzzy import fuzz, process
import numpy as np
import yagmail


# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")

def fuzzy_match(token, choices, threshold=80):
    match, score = process.extractOne(token, choices, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return match
    return None

def extract_caracteristicas(text):
    # Procesar el texto con spaCy
    doc = nlp(text.lower())
    found_caracteristicas_fisicas = {}
    found_personalidades = []
    found_categorias = None  # Cambiar found_categorias para que sea un valor escalar
    found_eventos = {}
    found_genero = ""

    # Convertir las características físicas, eventos y géneros a minúsculas para la comparación
    caracteristicas_fisicas_lower = {k.lower(): [v.lower() for v in vs] for k, vs in caracteristicas_fisicas.items()}
    eventos_lower = [e.lower() for e in Eventos["Evento"]]
    
    # Convertir géneros a minúsculas para comparación
    generos_m_lower = [g.lower() for g in generos['M']]
    generos_f_lower = [g.lower() for g in generos['F']]

    # Buscar personalidades en el texto usando fuzzy matching
    personalidades_lower = [p.lower() for p in personalidades]
    
    for token in doc:
        match = fuzzy_match(token.text.lower(), personalidades_lower)
        if match:
            found_personalidades.append(match)
    
    # Buscar categorías en el texto
    for token in doc:
        for categoria, valor in categorias.items():
            if categoria.lower() in token.text.lower():
                found_categorias = categoria  # Almacena el valor de la categoría encontrada
                break  # Rompe el bucle si se encuentra una categoría
          
    # Buscar características físicas en el texto usando fuzzy matching
    for key, values in caracteristicas_fisicas_lower.items():
        for token in doc:
            match = fuzzy_match(token.text.lower(), values)
            if match:
                found_caracteristicas_fisicas[key] = match
                break
        else:
            found_caracteristicas_fisicas[key] = 'Desconocido'  # Asignar 'Desconocido' si no se encuentra

    # Buscar el género en el texto usando fuzzy matching
    for token in doc:
        if fuzzy_match(token.text.lower(), generos_m_lower):
            found_genero = "hombre"
            break
        elif fuzzy_match(token.text.lower(), generos_f_lower):
            found_genero = "mujer"
            break

    # Buscar eventos en el texto usando fuzzy matching
    for token in doc:
        match = fuzzy_match(token.text.lower(), eventos_lower)
        if match:
            found_eventos[match] = match

    # Verificación de found_eventos
    if isinstance(found_eventos, dict):
        eventos_str = ', '.join(found_eventos.values()) or 'Desconocido'
    else:
        eventos_str = 'Desconocido'

    # Verificación de found_categorias
    found_categorias = found_categorias or 'Desconocido'

    # Crear el DataFrame
    df_data = {
        'Categoría': found_categorias ,
        'Género': found_genero or 'Desconocido',
        'Tono de piel': found_caracteristicas_fisicas.get('tono de piel', 'Desconocido') or 'Desconocido',
        'Forma del rostro': found_caracteristicas_fisicas.get('forma del rostro', 'Desconocido') or 'Desconocido',
        'Contextura física': found_caracteristicas_fisicas.get('contextura física', 'Desconocido') or 'Desconocido',
        'Longitud del cuello': found_caracteristicas_fisicas.get('longitud del cuello', 'Desconocido') or 'Desconocido',
        'Estatura': found_caracteristicas_fisicas.get('estatura', 'Desconocido') or 'Desconocido',       
        'personalidad': ', '.join(found_personalidades) or 'Desconocido',
        'Evento': eventos_str  # Verificación agregada
    }
    
    df = pd.DataFrame([df_data])
    
    return expand_all_columns(df)






def categorize_predictions(y_pred):
    # Invertir los diccionarios de etiquetas para obtener categoría a partir del índice
    #inverse_labels_Categoria = {v: k for k, v in categorias.items()}
    inverse_labels_SubCarpetas = {v: k for k, v in SubCarpeta.items()}
    #inverse_labels_Carpetas = {v: k for k, v in carpetas.items()}
    
    # Variables para almacenar las categorías
    Categoria = []
    Subcarpeta = []
    Carpetas = []

    # Iterar sobre cada predicción
    for pred in y_pred.astype(int):
        #categoria_idx = np.maximum(pred[0], 0)
        subcarpeta_idx = np.maximum(pred, 0)

        # Obtener la categoría de cada índice
        #categoria = inverse_labels_Categoria.get(categoria_idx, "Unknown")
        subcarpeta = inverse_labels_SubCarpetas.get(subcarpeta_idx, "Unknown")
        #carpetas = inverse_labels_Carpetas.get(subcarpeta_idx, "Unknown")

        # Agregar a las listas
      #  Carpetas.append(carpetas)
        Subcarpeta.append(subcarpeta)

    return subcarpeta


def enviar_correo(Edad, mensaje):
    yag = yagmail.SMTP('odiseorincon@gmail.com', 'zwts ittk yfpm cvmi')
    
    mensaje_html = f"""
        <html>
        <head>
            <style>
                body {{
                    background-color: #f3f4f6;
                    padding: 24px;
                    font-family: 'Arial', sans-serif;
                }}
                .card {{
                    max-width: 400px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 15px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }}
                .user-info {{
                    display: flex;
                    align-items: center;
                    gap: 16px;
                }}
                .user-info img {{
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                }}
                .user-details {{
                    display: flex;
                    flex-direction: column;
                }}
                .user-name {{
                    font-size: 20px;
                    font-weight: bold;
                    margin: 0;
                }}
                .user-age {{
                    color: #6b7280;
                    font-size: 14px;
                }}
                .message {{
                    margin-top: 16px;
                    color: #4b5563;
                    font-size: 16px;
                    line-height: 1.5;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="user-info">
                    <div class="user-details">
                        <p class="user-age">{Edad} años de Edad</p>
                    </div>
                </div>
                <div class="message">
                    {mensaje}
                </div>
            </div>
        </body>
        </html>
        """

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