import requests

# URL du service REST
URL = "http://localhost:8080/ords/hr/projet_overview/"

# Fonction pour récupérer les données
def fetch_data():
    try:
        # Requête GET vers l'URL REST
        response = requests.get(URL)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        data = response.json()  # Convertit la réponse en JSON

        # Vérifie si les données sont disponibles
        if "items" in data:
            print("Données récupérées avec succès.")
            return data["items"]  # Retourne la liste des résultats
        else:
            print("Format inattendu de la réponse JSON :", data)
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

# Fonction pour afficher les 10 premières lignes
def display_first_10_rows(data):
    if not data:
        print("Aucune donnée à afficher.")
        return

    print("\nAffichage des 10 premières lignes récupérées :\n")
    for i, row in enumerate(data[:10], start=1):
        print(f"Ligne {i}: {row}")

# Fonction principale
def main():
    print("Récupération des données depuis ORDS...")
    data = fetch_data()

    print("\nAffichage des données :")
    display_first_10_rows(data)

if __name__ == "__main__":
    main()
