from flask import Flask, request, jsonify, render_template
import base64
import pickle
import io
from PIL import Image, ImageOps
import numpy as np
import traceback  # Ajout pour afficher les erreurs détaillées
import os
from datetime import datetime
import psutil 
import sqlite3

SAVE_DIR = "saved_images"
os.makedirs(SAVE_DIR, exist_ok=True)



app = Flask(__name__)

# Charger le modèle entraîné
with open("digit_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)


def create_table():
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    
    # Créer la table si elle n'existe pas déjà
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label INTEGER NOT NULL,
            image BLOB NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

create_table()  # Créer la table lors du démarrage

def process_image(image_base64, label):
    """Transforme une image encodée en base64 en un tableau numpy formaté pour le modèle et enregistre l'image avec le label dans SQLite."""
    
    # Décoder l'image de base64
    image_data = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_data))

    # Traitement de l'image (convertir en niveau de gris, inverser, rogner et redimensionner)
    image = image.convert("L")
    image = ImageOps.invert(image)
    bbox = image.getbbox()
    image = image.crop(bbox) if bbox else image
    image = image.resize((8, 8))

    # Sauvegarder l'image traitée sous forme de tableau numpy pour la prédiction
    image_array = np.array(image).reshape(1, -1)

    # Enregistrer l'image et le label dans la base de données SQLite
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    # Insérer l'image et son label dans la base de données (en tant que BLOB)
    cursor.execute('''
        INSERT INTO images (label, image) VALUES (?, ?)
    ''', (label, sqlite3.Binary(image_data)))  # Utiliser `sqlite3.Binary` pour stocker l'image en tant que BLOB

    conn.commit()
    conn.close()

    return image_array

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        mem_info = psutil.virtual_memory()
        print(f"[INFO] Mémoire utilisée: {mem_info.percent}%")
        
        # Vérifier si on reçoit bien des données
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "Aucune image reçue"}), 400
        
        image_base64 = data["image"]
        label = int(data["label"]) 
        print("[INFO] Image reçue en base64")  # Log dans la console

        # Traiter l'image
        image_array = process_image(image_base64,label)
        print("[INFO] Image transformée en array numpy")  # Log

        # Faire la prédiction
        prediction = model.predict(image_array)
        proba = model.predict_proba(image_array)  # Probabilités pour chaque classe
        predicted_class = int(prediction[0])  # Classe prédite
        certainty = proba[0][predicted_class] * 100  # Probabilité associée à la classe prédite, en pourcentage

        print(f"[INFO] Prédiction faite : {prediction}, {proba}")  # Log
        
        # Vérification de la certitude (si inférieure à 60%, retourner une erreur)
        if certainty < 60:
            return jsonify({"error": "La certitude est trop faible pour une prédiction fiable. Essayez à nouveau."}), 400
        
        # Renvoi de la prédiction et de la certitude au frontend
        return jsonify({
            "prediction": predicted_class,
            "certainty": round(certainty, 2)  # Certitude arrondie à 2 décimales
        })
    
    except Exception as e:
        print("[ERROR]", traceback.format_exc())  # Affiche toute l'erreur
        return jsonify({"error": str(e)}), 500



@app.route('/api/system_info', methods=['GET'])
def system_info():
    try:
        mem_info = psutil.virtual_memory()
        cpu_info = psutil.cpu_percent(interval=1)  # Intervalle pour obtenir une estimation plus précise
        
        # Créer un dictionnaire avec les informations à renvoyer
        return jsonify({
            "memory": f"{mem_info.percent}%",
            "cpu": f"{cpu_info}%"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
