import os
from flask import Flask, request, render_template, jsonify
import joblib
from Funciones import (
    enviar_correo,
    extract_caracteristicas,
    categorize_predictions,
    get_images_from_folder
)
from vectorize import preprocess_and_vectorize
from labels import subCarpetaHombre, subCarpetaMujer

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

# Predicción
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    texto = data.get('texto')
    
    if not texto:
        return jsonify({'error': 'El texto es requerido'}), 400

    df = extract_caracteristicas(texto)
    model, vectorizador, subcarpeta = (
        (modelo_hombre, vectorizadorHombre, subCarpetaHombre) 
        if 'hombre' in texto else 
        (modelo_mujer, vectorizadorMujer, subCarpetaMujer)
    )
    
    df_final = preprocess_and_vectorize(df, vectorizador)
    prediccion = model.predict(df_final)
    categorias = categorize_predictions(prediccion, subcarpeta)

    # Preparar respuesta con imágenes por categoría
    respuesta = {
        f'images{idx if idx > 0 else ""}': get_images_from_folder(os.path.join('./static/Imágenes_joyería', categoria.replace(' ', '')))
        for idx, categoria in enumerate(categorias)
    }

    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
