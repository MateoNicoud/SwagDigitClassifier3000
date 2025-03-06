import sqlite3
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle
import os
from PIL import Image
import io

def load_data_from_db():
    """Charge les données (images et labels) depuis la base de données SQLite."""
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    # Récupérer les images et labels
    cursor.execute('SELECT label, image FROM images')
    data = cursor.fetchall()

    X = []
    y = []

    for label, image_data in data:
        # Convertir les données d'image en format que le modèle peut utiliser
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("L")  # Convertir en niveau de gris
        image = image.resize((8, 8))  # Redimensionner à 8x8 (taille standard pour les modèles de chiffres)
        image_array = np.array(image).reshape(1, -1)  # Applatir l'image en un vecteur
        X.append(image_array)
        y.append(label)

    conn.close()

    # Convertir en arrays numpy
    X = np.vstack(X)
    y = np.array(y)

    return X, y

# Charger les nouvelles données depuis la base de données
X, y = load_data_from_db()

# Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

print("Nombre d'éléments pour l'apprentissage:", len(X_train))
print("Nombre d'éléments pour les tests:", len(X_test))

# Créer et entraîner le modèle KNN avec les nouvelles données
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# Évaluer le modèle (facultatif)
accuracy = model.score(X_test, y_test)
print(f"Précision du modèle sur les données de test: {accuracy * 100:.2f}%")

# Sauvegarder le modèle mis à jour dans le fichier "digit_classifier.pkl"
with open(os.path.join(os.getcwd(), "digit_classifier.pkl"), "wb") as f:
    pickle.dump(model, f)

print("Le modèle a été mis à jour et sauvegardé dans 'digit_classifier.pkl'.")
