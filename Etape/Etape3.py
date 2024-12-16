import matplotlib.pyplot as plt
from Etape2 import fetch_random_10
from datetime import datetime

# Fonction pour normaliser les données
def normalize(values):
    min_val = min(values)
    max_val = max(values)
    if max_val - min_val == 0:  # Si les données sont constantes
        return [0.5 for _ in values]
    return [(v - min_val) / (max_val - min_val) for v in values]

def plot_data(data):
    """
    Affiche les données sous forme de graphique.
    """
    if not data:
        print("Aucune donnée à afficher.")
        return

    # Axe X basé sur les secondes
    seconds = list(range(10))
    oti = [d["oti"] for d in data]
    wti = [d["wti"] for d in data]
    oli = [d["oli"] for d in data]
    ati = [d["ati"] for d in data]

    # Normalisation des valeurs
    oti_normalized = normalize(oti)
    wti_normalized = normalize(wti)
    oli_normalized = normalize(oli)
    ati_normalized = normalize(ati)

    # Création du graphique avec axes secondaires
    fig, ax1 = plt.subplots(figsize=(12, 8))

    ax1.plot(seconds, oti_normalized, label="OTI (normalisé)", marker="o", linestyle="--", color="blue")
    ax1.plot(seconds, wti_normalized, label="WTI (normalisé)", marker="s", linestyle="-.", color="orange")
    ax1.plot(seconds, ati_normalized, label="ATI (normalisé)", marker="x", linestyle=":", color="purple")
    ax1.set_xlabel("Temps (secondes)", fontsize=14)
    ax1.set_ylabel("Valeurs normalisées (OTI, WTI, ATI)", fontsize=14, color="black")
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.grid(visible=True, linestyle="--", alpha=0.6)

    ax2 = ax1.twinx()
    ax2.plot(seconds, oli_normalized, label="OLI (normalisé)", marker="^", linestyle="-", color="green")
    ax2.set_ylabel("Valeurs normalisées (OLI)", fontsize=14, color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), fontsize=12)

    plt.title("Évolution des indicateurs sur 10 secondes (normalisés)", fontsize=16)
    plt.tight_layout()
    plt.show()

def run_plot():
    """
    Récupère les données et affiche le graphique.
    """
    data = fetch_random_10()
    plot_data(data)
