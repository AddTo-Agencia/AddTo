import os
from flask import Flask,send_from_directory, request, render_template, jsonify
import joblib
from Funciones import enviar_correo, extract_caracteristicas, categorize_predictions,get_images_from_folder,get_category_descriptions
from vectorize import preprocess_and_vectorize,preprocess_and_predict
from labels import categorias
# Instalar las librerías si no están

#Correo agencia addtoagencia@gmail.com

'''

def install_requirements():
    if os.path.exists('requirements.txt'):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("El archivo requirements.txt no se encontró. Por favor, asegúrate de que el archivo exista en el directorio.")
'''



# Cargar modelos previamente entrenados y guardados con joblib

modelo = joblib.load('./Models/model_x.pkl')
vectorizador = joblib.load('./Models/vectorizador.pkl')

# Crear una instancia de la aplicación Flask
app = Flask(__name__)


# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('Index.html')



@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/send', methods=['POST'])
def send():
    
    data = request.get_json()
    edad = data['edad']
    mensaje = data['mensaje']
    
    return jsonify(enviar_correo(edad,mensaje))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extraer datos JSON del cuerpo de la solicitud
        data = request.get_json()
        texto = data['texto']

        # Crear un DataFrame a partir de los datos JSON
        df = extract_caracteristicas(texto)
        print(df)
        # Procesar el DataFrame y vectorizar
        df_final = preprocess_and_vectorize(df, vectorizador)

        # Realizar la predicción
        prediccion = modelo.predict(df_final)
        print(prediccion)

        # Categorizar la predicción
        subcarpeta = categorize_predictions(prediccion)
        
        # Construir la ruta a las imágenes basándote en la subcarpeta
        path = './static/Imágenes_joyería/' + subcarpeta.replace(' ', '')
        
        print("Subcarpeta:", subcarpeta)
        
        # Buscar imágenes en la ruta
        imagenes = []
        if os.path.exists(path):
            print("Existe la ruta:", path)
            imagenes = get_images_from_folder(path)
        else:
            print("No existe la ruta:", path)

        # Preparar la respuesta
        respuesta = {
           # 'resultado': get_category_descriptions(categoria),
            'images': imagenes
        }

        return jsonify(respuesta)

    except Exception as e:
        # Manejar cualquier error que ocurra durante la predicción
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    print("server iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)
    