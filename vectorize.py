from nltk.tokenize import word_tokenize
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk, joblib, re, gc
import scipy.sparse as sp


# Descargar recursos necesarios de nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('spanish'))

    def lemmatize_and_tokenize(self, text):
        if not text.strip(): return ''
        text = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]', '', text.lower())
        tokens = word_tokenize(text)
        return ' '.join([self.lemmatizer.lemmatize(t) for t in tokens if t not in self.stop_words])

    def fit(self, X, y=None): return self

    def transform(self, X): return X.apply(self.lemmatize_and_tokenize)

def preprocess_and_vectorize(df, vectorizers=None):
    vectorizers = vectorizers or {}
    X_text_vectorized = None
    for col in df.columns:
        vectorizer = vectorizers.get(col, TfidfVectorizer(stop_words='spanish', min_df=1))
        if col not in vectorizers:
            vectorizer.fit(df[col])
            vectorizers[col] = vectorizer
        X_col_vectorized = vectorizer.transform(df[col])
        X_text_vectorized = sp.hstack([X_text_vectorized, X_col_vectorized]) if X_text_vectorized is not None else X_col_vectorized
        gc.collect()
    return X_text_vectorized

def preprocess_and_predict(df, model, vectorizer_path='./Models/vectorizador.pkl'):
    vectorizers = joblib.load(vectorizer_path)
    df = df.fillna('').astype(str)
    X_text_vectorized = [Pipeline([('vectorizer', vectorizers[col])]).transform(df[col]) for col in df.columns if col in vectorizers]
    if not X_text_vectorized: raise ValueError("No se pudieron vectorizar los datos.")
    X_combined = hstack(X_text_vectorized)
    return model.predict(X_combined)
