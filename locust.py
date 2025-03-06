
from locust import HttpUser, task, between
import base64
import json

# Charger une image de test et la convertir en base64
with open("test_digit.png", "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")


class LoadTestPredict(HttpUser):
    wait_time = between(1, 3)  # Temps d'attente aléatoire entre 1 et 3 secondes

    @task
    def send_image(self):
        """Envoie une image en base64 à l'API /api/predict"""
        payload = json.dumps({"image": base64_image})
        headers = {"Content-Type": "application/json"}

        response = self.client.post("/api/predict", data=payload, headers=headers)

        if response.status_code == 200:
            print(f"✅ Réponse : {response.json()}")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
