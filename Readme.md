# SwagDigitClassifier3000

Bienvenue dans **SwagDigitClassifier3000**, une application Flask permettant de prédire un chiffre (de 0 à 9) basé sur une image dessinée à la main. Le modèle de classification utilise un fichier `digit_classifier.pkl` préalablement formé à partir du fichier Jupyter Notebook `digits_par_jean-michel_version_0.3b.ipynb`.

## Fonctionnalités

- **Prédiction des chiffres** : Dessinez un chiffre sur un canevas et envoyez-le pour obtenir une prédiction accompagnée d'une mesure de certitude.
- **Interface utilisateur** : Utilisation d'un canevas HTML5 pour dessiner le chiffre, avec des boutons pour envoyer ou réinitialiser l'image.
- **Informations système** : Affichage en temps réel de l'utilisation du CPU et de la mémoire du serveur via une API `/api/system_info`.
- **API RESTful** : Une API POST `/api/predict` pour envoyer des images et obtenir les prédictions.

## Prérequis

1. **Python 3.13+** : Cette application utilise Python 3.13, donc assurez-vous que vous avez la bonne version installée.
2. **Docker** : Si vous souhaitez déployer l'application via Docker Compose.
3. **Poetry** : Gestionnaire de dépendances utilisé pour le projet.

## Installation

### 1. Cloner le projet

```bash
git clone https://votre-repository-url.git
cd SwagDigitClassifier3000
```

### 2. Créer un environnement virtuel et installer les dépendances avec **Poetry**

Nous utilisons **Poetry** pour la gestion des dépendances. Installez **Poetry** si ce n'est pas déjà fait et installez les dépendances du projet avec :

```bash
poetry install
```

### 3. Exécuter l'application en mode développeur

Pour lancer l'application Flask en mode développement, utilisez la commande suivante :

```bash
poetry run python -m flask --app main run
```

Cela démarre l'application Flask avec **debugging activé**. L'application sera accessible à l'adresse [http://localhost:5000](http://localhost:5000).

### 4. Télécharger le modèle pré-entraîné

Le fichier `digit_classifier.pkl` est nécessaire pour effectuer les prédictions. Assurez-vous de l'avoir dans le même répertoire que votre script `main.py`.

### 5. Lancer l'application avec Docker Compose

Si vous préférez utiliser **Docker Compose**, vous pouvez démarrer l'application avec la commande suivante :

```bash
docker-compose up --build
```

Cela construira l'image Docker en utilisant le `Dockerfile` et démarrera l'application Flask sur [http://localhost:5000](http://localhost:5000).

## Docker Compose

Le fichier `docker-compose.yml` décrit le service Docker pour l'application. Il contient une seule définition de service `swagdigit`, qui est construite à partir du Dockerfile du projet et expose le port 5000.

### Exemple de fichier `docker-compose.yml` :

```yaml
services:
  swagdigit:
    build: .
    ports:
      - "5000:5000"
```

### 1. Construire et exécuter avec Docker Compose

Si vous préférez utiliser Docker Compose, vous pouvez démarrer l'application avec la commande suivante :

```bash
docker-compose up --build
```

Cela construira l'image Docker et démarrera l'application Flask sur [http://localhost:5000](http://localhost:5000).

## Jupyter Notebook

Le modèle utilisé par cette application a été créé et exporté depuis un **Jupyter Notebook**. Le fichier **`digits_par_jean-michel_version_0.3b.ipynb`** contient toutes les étapes nécessaires pour entraîner le modèle et l'exporter au format **pickle** dans le fichier **`digit_classifier.pkl`**.

### Exécution du Notebook

Pour exécuter le notebook localement, suivez ces étapes :

1. Installez **Jupyter Notebook** :
   ```bash
   poetry add jupyter
   ```

2. Lancez **Jupyter Notebook** :
   ```bash
   poetry run jupyter notebook
   ```

3. Ouvrez le fichier **`digits_par_jean-michel_version_0.3b.ipynb`** et suivez les instructions pour entraîner le modèle et l'exporter dans le fichier **`digit_classifier.pkl`**.

## Structure du projet

```
SwagDigitClassifier3000/
├── app.py                    # Script principal de l'application Flask
├── digits_par_jean-michel_version_0.3b.ipynb  # Notebook Jupyter pour entraîner le modèle
├── digit_classifier.pkl      # Modèle de prédiction entraîné
├── Dockerfile                # Dockerfile pour le déploiement avec Docker
├── docker-compose.yml        # Fichier de configuration Docker Compose
├── pyproject.toml            # Fichier de configuration Poetry
├── poetry.lock               # Fichier de verrouillage des dépendances Poetry
├── .python-version           # Version de Python utilisée pour le projet
├── .gitignore                # Fichier gitignore pour ignorer certains fichiers
├── requirements.txt          # Dépendances nécessaires à l'exécution
└── README.md                 # Documentation du projet
```

## Endpoints API

### 1. `/api/predict` (POST)

- **Description** : Envoie une image en base64 pour obtenir une prédiction.
- **Request body** :
    ```json
    {
      "image": "data:image/png;base64,iVBORw0KGgoAAAANS..."
    }
    ```
- **Response** :
    ```json
    {
      "prediction": 5,
      "certainty": 75.32
    }
    ```
- **Error response** :
    ```json
    {
      "error": "La certitude est trop faible pour une prédiction fiable. Essayez à nouveau."
    }
    ```

### 2. `/api/system_info` (GET)

- **Description** : Obtient des informations système, y compris l'utilisation de la mémoire et du CPU.
- **Response** :
    ```json
    {
      "memory": "65%",
      "cpu": "45%"
    }
    ```

## Explications du Code

### 1. `main.py`

Le fichier `main.py` contient le code Flask pour l'API RESTful et la logique du modèle de classification.

- **Chargement du modèle** : Le modèle est chargé depuis un fichier `digit_classifier.pkl` à l'aide de **pickle**.
- **Traitement de l'image** : Les images sont reçues en base64, puis traitées (conversion en niveaux de gris, inversion, redimensionnement) avant d'être passées au modèle.
- **Prédiction et certitude** : Une prédiction est effectuée, et la certitude est renvoyée. Si la certitude est inférieure à 60%, une erreur est renvoyée.

#### Sauvegarde des images

Toutes les images envoyées depuis le frontend vers le backend sont **sauvegardées** dans un dossier nommé **`saved_images`**. Chaque image reçoit un nom unique basé sur un horodatage au moment où elle est reçue. Cela permet de conserver une trace de toutes les images traitées par l'application.

- **Dossier `saved_images`** : Les images reçues en base64 sont converties en fichiers PNG et sauvegardées à cet emplacement.

### 2. `index.html`

Cette page HTML contient un canevas où les utilisateurs peuvent dessiner un chiffre, ainsi que des boutons pour envoyer l'image ou la réinitialiser. Le résultat de la prédiction est affiché après l'envoi de l'image.

### 3. `Dockerfile`

Le Dockerfile permet de construire un container pour déployer l'application. Il utilise **gunicorn** comme serveur WSGI pour Flask et expose le port 5000 pour l'accès à l'application.

## Test de charge

Vous pouvez lancer locust avec la commande : 
```bash
poetry run locust -f locust.py --host=http://localhost:5000
``