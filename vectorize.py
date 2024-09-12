from nltk.tokenize import word_tokenize
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from scipy.sparse import hstack
import nltk
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import gc
import scipy.sparse as sp

# Descargar stopwords si es necesario
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

#vectorizador 

# Clase personalizada para Preprocesamiento de Texto
class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('spanish'))  # Stop words en español

    def lemmatize_and_tokenize(self, text):
        if not text or text.strip() == '':
            return ''
        # Eliminar caracteres especiales y convertir a minúsculas
        text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]', '', text.lower())
        tokens = word_tokenize(text)
        # Filtrar stop words y lematizar
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        return ' '.join(lemmatized_tokens)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self.lemmatize_and_tokenize)






# Función para vectorizar las columnas de texto
def preprocess_and_vectorize(df, vectorizers=None):
    if vectorizers is None:
        vectorizers = {}

    X_text_vectorized = None

    # Procesar columna por columna
    for col in df.columns:
        if col in vectorizers:
            # Usar vectorizador existente
            vectorizer = vectorizers[col]
            X_col_vectorized = vectorizer.transform(df[col])
        else:
            # Crear nuevo vectorizador si no existe
            vectorizer = TfidfVectorizer(stop_words=stopwords.words('spanish'), min_df=1)
            vectorizer.fit(df[col])
            X_col_vectorized = vectorizer.transform(df[col])
            vectorizers[col] = vectorizer

        # Concatenar las matrices en una sola (si es la primera, inicializarla)
        if X_text_vectorized is None:
            X_text_vectorized = X_col_vectorized
        else:
            X_text_vectorized = sp.hstack([X_text_vectorized, X_col_vectorized])

        gc.collect()  # Liberar memoria después de cada columna

    return X_text_vectorized

# Clase para seleccionar una columna específica de un DataFrame


def preprocess_and_predict(df, model, vectorizer_path='./Models/vectorizador.pkl'):
    """
    Preprocesa los datos y realiza predicciones usando un modelo entrenado.
    
    Args:
    df (pd.DataFrame): Los datos que se van a predecir.
    model: El modelo entrenado.
    vectorizer_path (str): Ruta al archivo que contiene los vectorizadores entrenados.
    
    Returns:
    array: Predicciones del modelo.
    """
    # Cargar vectorizadores previamente entrenados
    vectorizers = joblib.load(vectorizer_path)
    
    # Convertir todas las columnas a texto (esto asegura compatibilidad)
    df = df.fillna('').astype(str)
    
    # Inicializar lista para las columnas vectorizadas
    X_text_vectorized = []
    
    # Aplicar los vectorizadores a cada columna
    for col in df.columns:
        if col in vectorizers:
            # Usar el vectorizador proporcionado
            vectorizer = vectorizers[col]
            # Crear un pipeline solo para la vectorización
            pipeline = Pipeline([('vectorizer', vectorizer)])
            # Aplicar el vectorizador a la columna
            X_col_vectorized = pipeline.transform(df[col])
            X_text_vectorized.append(X_col_vectorized)
        else:
            raise ValueError(f"No se encontró un vectorizador para la columna '{col}'")
    
    # Combinar todas las columnas vectorizadas en una sola matriz de características
    if X_text_vectorized:
        X_combined = hstack(X_text_vectorized)
    else:
        X_combined = None
    
    # Verificar que haya datos vectorizados
    if X_combined is None:
        raise ValueError("No se pudieron vectorizar los datos.")
    
    # Realizar predicciones con el modelo
    predictions = model.predict(X_combined)
    
    return predictions