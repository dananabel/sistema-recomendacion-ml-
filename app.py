import pickle
from surprise import *
from surprise.model_selection import *
from sklearn.metrics.pairwise import *
from sklearn.metrics import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from math import sqrt
from sklearn.decomposition import TruncatedSVD
from flask import Flask, request, jsonify, render_template
import os
import requests
import gdown

app = Flask(__name__)

# 🔗 ID de tu modelo en Google Drive
GOOGLE_DRIVE_FILE_ID = "1KAsHO0E0Bw_Lz5w5JReb34nTniKC7vdA"

def download_model():
    """Descarga el modelo desde Google Drive si no existe localmente"""
    if not os.path.exists("svd_modelo.pkl"):
        print("📥 Descargando modelo desde Google Drive...")
        try:
            # Formato correcto para gdown
            gdown.download(f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}", 
                          "svd_modelo.pkl", quiet=False)
            print("✅ Modelo descargado exitosamente")
        except Exception as e:
            print(f"❌ Error descargando modelo: {str(e)}")
            return False
    return True

def load_model():
    """Carga el modelo SVD"""
    try:
        # Primero intenta descargar si no existe
        if not download_model():
            return None
            
        with open("svd_modelo.pkl", 'rb') as file:
            model = pickle.load(file)
        print("✅ Modelo cargado exitosamente")
        return model
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo svd_modelo.pkl")
        return None
    except Exception as e:
        print(f"❌ Error cargando el modelo: {str(e)}")
        return None

# 📦 Cargar el modelo al iniciar la app
svd_model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global svd_model
    
    # Cargar modelo si no está en memoria
    if svd_model is None:
        svd_model = load_model()
    
    if svd_model is None:
        return render_template('result.html',
                                user_id="N/A",
                                product_id="N/A",
                                prediction="Error: Modelo no disponible")
    
    user_id = request.form.get('user_id')
    product_id = request.form.get('product_id')
    
    if not user_id or not product_id:
        return render_template('result.html',
                                user_id=user_id or "N/A",
                                product_id=product_id or "N/A",
                                prediction="Error: Faltan datos requeridos")
    
    try:
        prediction = svd_model.predict(uid=user_id, iid=product_id)
        predicted_rating = round(prediction.est, 2)
        
        return render_template('result.html',
                                user_id=user_id,
                                product_id=product_id,
                                prediction=predicted_rating)
    
    except Exception as e:
        print(f"❌ Error en predicción: {str(e)}")
        return render_template('result.html',
                                user_id=user_id,
                                product_id=product_id,
                                prediction=f"Error: {str(e)}")

# 🚀 CONFIGURACIÓN CRÍTICA PARA RAILWAY
if __name__ == "__main__":
    # Para desarrollo local
    app.run(debug=True, port=5000)
else:
    # Para Railway - EXACTAMENTE como dice la documentación
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
