import requests

# URL du service REST
URL = "http://localhost:8080/ords/hr/projet/projet_internal_random"

def fetch_random_10():
    """
    Récupère 10 lignes aléatoires depuis l'API REST.
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()  # Convertit la réponse en JSON
        print("10 lignes récupérées avec succès.")
        return data["items"]  # Retourne les données
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []
