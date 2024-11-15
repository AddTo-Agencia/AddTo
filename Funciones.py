from features import personalidades, caracteristicas_fisicas, Eventos, generos
import spacy
import pandas as pd
from labels import carpetas,categorias,SubCarpeta,subCarpetaHombre,subCarpetaMujer
import os
from fuzzywuzzy import fuzz, process
import yagmail
#from transformers import pipeline
import random
from vistahtml import vistaHtml
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el modelo de lenguaje en español
nlp = spacy.load("es_core_news_sm")

#classifier1 = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

def fuzzy_match(token, choices, threshold=80):
    match, score = process.extractOne(token, choices, scorer=fuzz.token_sort_ratio)
    return match if score >= threshold else None

def extract_caracteristicas(text):
    doc = nlp(text.lower())
    default = 'Desconocido'

    # Preparar datos para comparación
    caracteristicas_lower = {k.lower(): [v.lower() for v in vs] for k, vs in caracteristicas_fisicas.items()}
    eventos_lower = [e.lower() for e in Eventos["Evento"]]
    generos_m_lower, generos_f_lower = [g.lower() for g in generos['M']], [g.lower() for g in generos['F']]
    personalidades_lower = [p.lower() for p in personalidades]

    # Buscar personalidades
    found_personalidades = list(filter(None, (fuzzy_match(token.text, personalidades_lower) for token in doc)))

    # Buscar categoría
    found_categorias = next((cat for token in doc for cat in categorias if cat.lower() in token.text.lower()), None)

    # Características físicas
    found_caracteristicas = {k: next((fuzzy_match(token.text, vs) for token in doc if fuzzy_match(token.text, vs)), default)
                             for k, vs in caracteristicas_lower.items()}

    # Género
    found_genero = ("hombre" if any(fuzzy_match(token.text, generos_m_lower) for token in doc) 
                    else "mujer" if any(fuzzy_match(token.text, generos_f_lower) for token in doc) else "")

    # Eventos
    found_eventos = {token.text.lower(): fuzzy_match(token.text.lower(), eventos_lower) for token in doc if fuzzy_match(token.text.lower(), eventos_lower)}
    eventos_str = ', '.join(found_eventos.values()) or default

    # Crear DataFrame
    df_data = {
        'Categoría': detectar_categoria_subcarpeta(text)['categoria'],
        'Tono de piel': found_caracteristicas.get('tono de piel', default),
        'Forma del rostro': found_caracteristicas.get('forma del rostro', default),
        'Contextura física': found_caracteristicas.get('contextura física', default),
        'Longitud del cuello': found_caracteristicas.get('longitud del cuello', default),
        'Estatura': found_caracteristicas.get('estatura', default),
        'personalidad': ', '.join(found_personalidades) or default,
        'Evento': eventos_str
    }
    
    return expand_all_columns(pd.DataFrame([df_data]))



def categorize_predictions(y_pred, labels):
    # Invertir el diccionario de etiquetas
    inverse_labels = {v: k for k, v in labels.items()}
    # Obtener subcarpetas eliminando duplicados
    return list(set(inverse_labels.get(int(pred), "Unknown") for pred in y_pred))

def enviar_correo(edad, mensaje):
   
    yag = yagmail.SMTP('odiseorincon@gmail.com', 'zwts ittk yfpm cvmi')
    try:
        yag.send(to='addtoagencia@gmail.com', subject='Datos Sobre Usuario', contents=vistaHtml(mensaje, edad))
        return "Correo enviado correctamente."
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"



def get_images_from_folder(folder_path):
    folder_path = './static/Imágenes_joyería/'+folder_path
    if os.path.isdir(folder_path):
        return [
            os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'))
        ]
    return []


'''

'''
vectorizer = TfidfVectorizer()


# Función para detectar la categoría más cercana utilizando similitud de coseno
def detectar_categoria_subcarpeta(texto_usuario):
    # Detectamos el género del usuario buscando palabras clave en el texto
    genero = "hombre" if re.search(r"\bhombre\b", texto_usuario, re.IGNORECASE) else "mujer"
    
    # Convertir las categorías a una lista
    categorias_list = list(categorias.keys())
    
    # Combinar el texto del usuario con las categorías para la vectorización
    documentos = categorias_list + [texto_usuario]  # Añadir el texto del usuario al final
    
    # Convertir los textos en vectores TF-IDF
    tfidf_matrix = vectorizer.fit_transform(documentos)
    
    # Calcular la similitud de coseno entre el texto del usuario y las categorías
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Encontrar la categoría con mayor similitud
    categoria_detectada = categorias_list[cosine_similarities.argmax()]
    
    return {"categoria": categoria_detectada, "genero_detectado": genero}

    

'''
def obtener_subcarpeta(genero, descripcion):
    subcarpetas = subCarpetaHombre if genero.lower() == 'hombre' else subCarpetaMujer if genero.lower() == 'mujer' else None
    return classifier1(descripcion, subcarpetas)["labels"][0] if subcarpetas else "Género no reconocido"

'''


def obtener_subcarpeta_r(genero, categoria):
    subcarpetas = (subCarpetaHombre if genero.lower() == 'hombre' 
                   else subCarpetaMujer if genero.lower() == 'mujer' 
                   else None)

    if not subcarpetas:
        return "Género no reconocido"

    categorias = {
        'Anillo de boda': ['Anillo_boda_hombre / A', 'Anillo_boda_hombre / B', 'Anillo_boda_hombre / C', 'Anillo_boda_hombre / D', 'Anillo_boda_mujer / A', 'Anillo_boda_mujer / B'],
        'Anillo de compromiso': ['Anillo_compromiso_mujer / A', 'Anillo_compromiso_mujer / B', 'Anillo_compromiso_mujer / C', 'Anillo_compromiso_mujer / D'],
        'Anillo': ['Anillos_masculinos / A', 'Anillos_masculinos / B', 'Anillos_masculinos / C', 'Anillos_femeninos / A', 'Anillos_femeninos / B'],
        'Collar con colgante': ['Collar_colgante_femenino / A', 'Collar_colgante_femenino / B', 'Collar_colgante_femenino / C'],
        'Collar de perlas': ['Collar_perlas_femenino / A', 'Collar_perlas_femenino / B', 'Collar_perlas_femenino / C', 'Collar_perlas_femenino / D'],
        'Gargantillas femeninas': ['Gargantillas_femeninas / A', 'Gargantillas_femeninas / B'],
        'Pulsera masculina': ['pulsera_masculina / A', 'pulsera_masculina / B', 'pulsera_masculina / C', 'pulsera_masculina / D'],
        'Reloj masculino': ['reloj_masculino / A', 'reloj_masculino / B', 'reloj_masculino / C', 'reloj_masculino / D']
    }

    subcarpetas_categoria = categorias.get(categoria)
    if not subcarpetas_categoria:
        return "Categoría no reconocida"

    subcarpetas_filtradas = [sub for sub in subcarpetas if sub in subcarpetas_categoria]
    return random.choice(subcarpetas_filtradas) if subcarpetas_filtradas else "No se encontraron subcarpetas para esta combinación"


'''
def obtener_subcarpeta(genero, descripcion):
    subcarpetas = subCarpetaHombre if genero.lower() == 'hombre' else subCarpetaMujer if genero.lower() == 'mujer' else None
    return classifier1(descripcion, subcarpetas)["labels"][0] if subcarpetas else "Género no reconocido"
'''


def split_column_and_expand(df, column):
    df[column] = df[column].astype(str).str.lower().str.split(',').explode().str.strip()
    return df[df[column].notna() & (df[column] != '')]

def expand_all_columns(df):
    for col in df.columns:
        if df[col].str.contains(',').any():
            df = split_column_and_expand(df, col)
    return df




