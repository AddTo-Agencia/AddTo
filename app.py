import os
from flask import Flask, send_from_directory, request, render_template, jsonify
import joblib
from Funciones import (
    enviar_correo,
    extract_caracteristicas,
    categorize_predictions,
    get_images_from_folder,
    get_category_descriptions
)
from vectorize import preprocess_and_vectorize
from labels import carpetas,categorias,SubCarpeta,subCarpetaHombre,subCarpetaMujer


# Cargar los modelos y vectorizador
#modelo = joblib.load('./Models/model_x.pkl')

modelo_mujer = joblib.load('./Models/model_x_mujer.pkl')
modelo_hombre = joblib.load('./Models/model_x_hombre (1).pkl')

vectorizadorMujer = joblib.load('./Models/vectorizadorMujer.pkl')
vectorizadorHombre = joblib.load('./Models/vectorizadorHombre.pkl')


# Crear una instancia de la aplicación Flask
app = Flask(__name__)

app.config['DEBUG'] = True

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('Index.html')


# Ruta para servir archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


# Ruta para enviar correos
@app.route('/send', methods=['POST'])
def send():
    try:
        data = request.get_json()
        edad = data.get('edad')
        mensaje = data.get('mensaje')
        
        # Validar que los datos estén presentes
        if not edad or not mensaje:
            return jsonify({'error': 'Faltan datos'}), 400
        
        # Llamada a la función para enviar el correo
        respuesta = enviar_correo(edad, mensaje)
        return jsonify(respuesta)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Ruta para realizar predicciones
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extraer los datos del cuerpo de la solicitud
        data = request.get_json()
        texto = data.get('texto')

        # Validar que el texto esté presente
        if not texto:
            return jsonify({'error': 'El texto es requerido'}), 400

        # Extraer características y procesar el texto
        df = extract_caracteristicas(texto)

        vectorizador = {}

        # Determinar el modelo y las subcarpetas según el género
        if 'hombre' in texto:
            model = modelo_hombre
            subcarpeta = subCarpetaHombre
            vectorizador = vectorizadorHombre
        else:
            model = modelo_mujer
            subcarpeta = subCarpetaMujer
            vectorizador = vectorizadorMujer

        # Preprocesar y vectorizar los datos
        df_final = preprocess_and_vectorize(df, vectorizador)
       
        # Realizar la predicción
        prediccion = model.predict(df_final)
        print(f"Predicción: {prediccion}")

        # Categorizar la predicción
        categorias = categorize_predictions(prediccion, subcarpeta)
        print(f"Categorías: {categorias}")

        # Preparar el diccionario de respuesta dinámicamente
        respuesta = {}

        # Para cada categoría, buscar imágenes y añadirlas al diccionario de respuesta
        for idx, categoria in enumerate(categorias):
            # Construir la ruta a las imágenes para cada categoría
            path = os.path.join('./static/Imágenes_joyería', categoria.replace(' ', ''))
            print(f"Ruta de imágenes para la categoría {categoria}: {path}")

            # Obtener las imágenes de la carpeta correspondiente
            imagenes = []
            if os.path.exists(path):
                imagenes = get_images_from_folder(path)
                print(f"Imágenes encontradas para la categoría {categoria}: {imagenes}")
            else:
                print(f"No existe la ruta: {path}")

            # Añadir las imágenes encontradas a la respuesta con claves dinámicas (images, images1, images2, ...)
            respuesta[f'images{idx if idx > 0 else ""}'] = imagenes

        return jsonify(respuesta)

    except Exception as e:
        # Capturar errores y responder adecuadamente
        print(f"Error durante la predicción: {e}")
        return jsonify({'error': 'Ocurrió un error durante la predicción. Inténtalo de nuevo.'}), 500




# Ejecutar la aplicación Flask
if __name__ == '__main__':
    print("Servidor iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)
