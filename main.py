import requests
import matplotlib.pyplot as plt


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

# Fonction pour normaliser les données
def normalize(values):
    min_val = min(values)
    max_val = max(values)
    if max_val - min_val == 0:  # Si les données sont constantes
        return [0.5 for _ in values]  # Retourne une constante normalisée
    return [(v - min_val) / (max_val - min_val) for v in values]

# Fonction pour afficher les données sous forme de graphique
def plot_data(data):
    if not data:
        print("Aucune donnée à afficher.")
        return

    # Axe X basé sur les secondes
    seconds = list(range(10))  # 0 à 9 pour représenter les 10 dernières secondes
    oti = [d["oti"] for d in data]
    wti = [d["wti"] for d in data]
    oli = [d["oli"] for d in data]
    ati = [d["ati"] for d in data]  # Ajout du champ ATI

    # Normalisation des valeurs pour éviter les chevauchements
    oti_normalized = normalize(oti)
    wti_normalized = normalize(wti)
    oli_normalized = normalize(oli)
    ati_normalized = normalize(ati)

    # Création du graphique avec axes secondaires
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Tracer les séries normalisées
    ax1.plot(seconds, oti_normalized, label="OTI (normalisé)", marker="o", linestyle="--", color="blue")
    ax1.plot(seconds, wti_normalized, label="WTI (normalisé)", marker="s", linestyle="-.", color="orange")
    ax1.plot(seconds, ati_normalized, label="ATI (normalisé)", marker="x", linestyle=":", color="purple")
    ax1.set_xlabel("Temps (secondes)", fontsize=14)
    ax1.set_ylabel("Valeurs normalisées (OTI, WTI, ATI)", fontsize=14, color="black")
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.grid(visible=True, linestyle="--", alpha=0.6)

    # Ajouter un deuxième axe Y pour OLI
    ax2 = ax1.twinx()
    ax2.plot(seconds, oli_normalized, label="OLI (normalisé)", marker="^", linestyle="-", color="green")
    ax2.set_ylabel("Valeurs normalisées (OLI)", fontsize=14, color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    # Ajouter une légende pour les deux axes
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), fontsize=12)

    # Annotation des points pour plus de clarté
    for i, (s, oti_val, wti_val, oli_val, ati_val) in enumerate(zip(seconds, oti_normalized, wti_normalized, oli_normalized, ati_normalized)):
        ax1.annotate(f"{oti[i]:.2e}", (s, oti_val), textcoords="offset points", xytext=(-10, 10), ha="center", fontsize=8)
        ax1.annotate(f"{wti[i]:.2e}", (s, wti_val), textcoords="offset points", xytext=(10, -15), ha="center", fontsize=8)
        ax1.annotate(f"{ati[i]:.2e}", (s, ati_val), textcoords="offset points", xytext=(10, 10), ha="center", fontsize=8)
        ax2.annotate(f"{oli[i]:.2e}", (s, oli_val), textcoords="offset points", xytext=(-10, -10), ha="center", fontsize=8)

    # Ajouter le titre
    plt.title("Évolution des indicateurs sur 10 secondes (normalisés)", fontsize=16)
    plt.tight_layout()

    # Afficher le graphique
    plt.show()

# Fonction principale
def main():
    print("Récupération des 10 lignes aléatoires...")
    data = fetch_random_10()

    print("\nAffichage des données :")
    for i, row in enumerate(data, start=1):
        print(f"Ligne {i}: {row}")

    print("\nAffichage graphique des données...")
    plot_data(data)

if __name__ == "__main__":
    main()
