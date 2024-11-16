from features import personalidades, caracteristicas_fisicas, Eventos, generos
import spacy
import pandas as pd
from labels import carpetas,categorias,SubCarpeta,subCarpetaHombre,subCarpetaMujer
import os
from fuzzywuzzy import fuzz, process
import yagmail
import random 
from vistahtml import vistaHtml

# Cargar el modelo de lenguaje en español 
nlp = spacy.load("es_core_news_sm")


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

    # Características físicas
    found_caracteristicas = {k: next((fuzzy_match(token.text, vs) for token in doc if fuzzy_match(token.text, vs)), default)
                             for k, vs in caracteristicas_lower.items()}

    # Eventos
    found_eventos = {token.text.lower(): fuzzy_match(token.text.lower(), eventos_lower) for token in doc if fuzzy_match(token.text.lower(), eventos_lower)}
    eventos_str = ', '.join(found_eventos.values()) or default

    # Crear DataFrame
    df_data = {
        'Categoría': detectar_categoria(text),
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

def enviar_correo(edad, mensaje, destinatario='addtoagencia@gmail.com'):
    try:
        yag = yagmail.SMTP('odiseorincon@gmail.com', 'zwts ittk yfpm cvmi')
        yag.send(to=destinatario, subject='Datos Sobre Usuario', contents=mensaje)
        return "Correo enviado correctamente."
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"

def get_images_from_folder(folder_path):
    return [
        os.path.join(folder_path, f) for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

def detectar_categoria(texto_usuario, categorias):
    texto_usuario = texto_usuario.lower()
    for categoria in categorias:
        if categoria.lower() in texto_usuario:
            return categoria
    return "No se encontró una categoría."

def obtener_subcarpeta_r(genero, categoria, subcarpetas_dict):
    subcarpetas = subcarpetas_dict.get(genero.lower(), [])
    return random.choice(subcarpetas.get(categoria, ["No disponible"]))

def expand_all_columns(df):
    for col in df.columns:
        if ',' in str(df[col].iloc[0]):
            df[col] = df[col].astype(str).str.split(',').explode().str.strip()
    return df
