import sqlite3

def init_db():
    """Initialise la base de données et crée la table images avec une colonne pour le label."""
    conn = sqlite3.connect('images.db')  # Connecte ou crée la base de données
    c = conn.cursor()

    # Crée la table 'images' si elle n'existe pas déjà, avec une colonne 'label' pour le chiffre associé
    c.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image BLOB,
        label INTEGER
    )''')

    conn.commit()
    conn.close()

# Appeler cette fonction une seule fois lors du démarrage de l'application
init_db()

# Exemple de fonction pour ajouter une image à la base de données
def add_image_to_db(image_data, label):
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO images (label, image) VALUES (?, ?)
    ''', (label, sqlite3.Binary(image_data)))  # Utiliser sqlite3.Binary pour stocker l'image

    conn.commit()
    conn.close()

# Exemple d'appel pour tester
# add_image_to_db(image_data, label)  # Remplacer `image_data` et `label` par tes données
