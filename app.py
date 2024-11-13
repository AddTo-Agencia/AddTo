import os
from flask import Flask, request, render_template, jsonify
import joblib
from Funciones import (
    enviar_correo,
    extract_caracteristicas,
    categorize_predictions,
    obtener_subcarpeta_r,
    get_images_from_folder
)
from vectorize import preprocess_and_vectorize
from labels import subCarpetaHombre, subCarpetaMujer
import scipy
import pandas as pd


# Cargar modelos y vectorizadores
modelo_mujer = joblib.load('./Models/model_x_mujer.pkl')
modelo_hombre = joblib.load('./Models/model_x_hombre (1).pkl')
vectorizadorMujer = joblib.load('./Models/vectorizadorMujer.pkl')
vectorizadorHombre = joblib.load('./Models/vectorizadorHombre.pkl')

app = Flask(__name__)

# Página de inicio
@app.route('/')
def home():
    return render_template('Index.html')

# Enviar correos
@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    edad = data.get('edad')
    mensaje = data.get('mensaje')
    
    if not edad or not mensaje:
        return jsonify({'error': 'Faltan datos'}), 400
    
    respuesta = enviar_correo(edad, mensaje)
    return jsonify(respuesta)



@app.route('/predict', methods=['POST'])
def predict():
    # Obtener datos JSON y extraer el texto proporcionado
    data = request.get_json()
    texto = data.get('texto')
    
    if not texto:
        return jsonify({'error': 'El texto es requerido'}), 400

    # Extracción de características
    try:
        df = extract_caracteristicas(texto)
    except Exception as e:
        return jsonify({'error': f'Error al extraer características: {str(e)}'}), 500

    # Determinar el género y seleccionar el modelo y vectorizador adecuados
    genero = 'hombre' if 'hombre' in texto.lower() else 'mujer'
    model, vectorizador, subcarpeta = (
        (modelo_hombre, vectorizadorHombre, subCarpetaHombre) 
        if genero == 'hombre' else 
        (modelo_mujer, vectorizadorMujer, subCarpetaMujer)
    )
    
    try:
        # Procesar y vectorizar el DataFrame de características
        df_final = preprocess_and_vectorize(df, vectorizador)
        
        # Convertir a DataFrame si la matriz es dispersa
        if isinstance(df_final, scipy.sparse.csr_matrix):
            df_final = pd.DataFrame(df_final.toarray())
        
        # Realizar la predicción
        prediccion = model.predict(df_final)
        print(df)
        
        # Clasificar las predicciones en categorías
        categorias = categorize_predictions(prediccion, subcarpeta)
        print('Categoria', categorias)
        
    except Exception as e:
        return jsonify({'error': f'Error en la predicción: {str(e)}'}), 500
    
    # Clasificación adicional para subcarpetas si es relevante

    # Preparar respuesta, incluyendo imágenes por cada categoría
    respuesta = {}
    for idx, categoria in enumerate(categorias):
        categoria_key = f'images{idx if idx > 0 else ""}'
        respuesta[categoria_key] = get_images_from_folder(categoria.replace(' ', ''))
    
    if df['Categoría'][0] and df['Categoría'][0] != 'Desconocido':
     print(obtener_subcarpeta_r(genero, df['Categoría'][0]))
     busqueda = obtener_subcarpeta_r(genero, df['Categoría'][0])
    else:
     busqueda = {}


    # Agregar resultados de la búsqueda a la respuesta si están disponibles
    if busqueda:
        respuesta['images_busqueda'] = get_images_from_folder(busqueda.replace(' ', ''))
    
    return jsonify(respuesta)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
