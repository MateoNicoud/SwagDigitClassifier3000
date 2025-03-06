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

SAVE_DIR = "saved_images"
os.makedirs(SAVE_DIR, exist_ok=True)



app = Flask(__name__)

# Charger le modèle entraîné
with open("digit_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

def process_image(image_base64):
    """Transforme une image encodée en base64 en un tableau numpy formaté pour le modèle."""
    image_data = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_data))

    # Sauvegarde de l'image originale
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_path = os.path.join(SAVE_DIR, f"original_{timestamp}.png")
    image.save(original_path)

    # Traitement de l'image
    image = image.convert("L")
    image = ImageOps.invert(image)
    bbox = image.getbbox()
    image = image.crop(bbox) if bbox else image
    image = image.resize((8, 8))

    # Sauvegarde de l'image traitée
    processed_path = os.path.join(SAVE_DIR, f"processed_{timestamp}.png")
    image.save(processed_path)

    # Transformation en array numpy
    image_array = np.array(image).reshape(1, -1)

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
        print("[INFO] Image reçue en base64")  # Log dans la console

        # Traiter l'image
        image_array = process_image(image_base64)
        print("[INFO] Image transformée en array numpy")  # Log

        # Faire la prédiction
        prediction = model.predict(image_array)
        proba = model.predict_proba(image_array)
        print(f"[INFO] Prédiction faite : {prediction}, {proba}")  # Log

        return jsonify({"prediction": int(prediction[0])})
    
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
