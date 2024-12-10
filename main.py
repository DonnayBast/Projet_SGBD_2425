import requests

# URL du service REST
URL = "http://localhost:8080/ords/hr/projet/projet_internal_random"

# Fonction pour récupérer les 10 lignes aléatoires
def fetch_random_10():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()  # Convertit la réponse en JSON
        print("10 lignes récupérées avec succès.")
        return data["items"]  # Retourne les données
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

# Fonction principale
def main():
    print("Récupération des 10 lignes aléatoires...")
    data = fetch_random_10()

    print("\nAffichage des données :")
    for i, row in enumerate(data, start=1):
        print(f"Ligne {i}: {row}")

if __name__ == "__main__":
    main()
