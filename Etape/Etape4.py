import requests
import matplotlib.pyplot as plt
import base64
import datetime
from PIL import Image
from io import BytesIO

# URL des endpoints REST
URL = "http://localhost:8080/ords/hr/projet/projet_internal_random"
POST_URL = "http://localhost:8080/ords/hr/snapshots/upload"
GET_URL = "http://localhost:8080/ords/hr/snapshots/retrieve"

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

# Fonction pour afficher et sauvegarder le graphique
def plot_data_and_save(data, filename="snapshot.png", resize_width=500, resize_height=250):
    if not data:
        print("Aucune donnée à afficher.")
        return

    # Axe X basé sur les secondes
    seconds = list(range(10))
    oti = [d["oti"] for d in data]
    wti = [d["wti"] for d in data]
    oli = [d["oli"] for d in data]
    ati = [d["ati"] for d in data]

    # Normalisation des données
    oti_normalized = normalize(oti)
    wti_normalized = normalize(wti)
    oli_normalized = normalize(oli)
    ati_normalized = normalize(ati)

    # Création du graphique
    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax1.plot(seconds, oti_normalized, label="OTI (normalisé)", marker="o", linestyle="--", color="blue")
    ax1.plot(seconds, wti_normalized, label="WTI (normalisé)", marker="s", linestyle="-.", color="orange")
    ax1.plot(seconds, ati_normalized, label="ATI (normalisé)", marker="x", linestyle=":", color="purple")
    ax1.set_xlabel("Temps (secondes)")
    ax1.set_ylabel("Valeurs normalisées (OTI, WTI, ATI)")

    ax2 = ax1.twinx()
    ax2.plot(seconds, oli_normalized, label="OLI (normalisé)", marker="^", linestyle="-", color="green")
    ax2.set_ylabel("Valeurs normalisées (OLI)")

    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.title("Évolution des indicateurs sur 10 secondes")
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Graphique sauvegardé sous : {filename}")

    # Sauvegarde du graphique
    with Image.open(filename) as img:
        img = img.resize((resize_width, resize_height))
        img.save(filename, optimize=True, quality=85)  # Compression supplémentaire
    print(f"Graphique sauvegardé et optimisé sous : {filename}")

# Fonction pour encoder une image en Base64
def encode_image_to_base64(filepath):
    try:
        # Convertir en JPEG avant encodage
        with Image.open(filepath) as img:
            img = img.convert("RGB")  # Conversion nécessaire pour JPEG
            jpeg_path = filepath.replace(".png", ".jpg")
            img.save(jpeg_path, "JPEG", quality=85)  # Compression JPEG
            with open(jpeg_path, "rb") as jpeg_file:
                encoded = base64.b64encode(jpeg_file.read()).decode("utf-8")
                return encoded
    except Exception as e:
        print(f"Erreur lors de l'encodage : {e}")
        return None
# Fonction pour envoyer le snapshot via POST à ORDS
def send_snapshot_to_db(image_base64):
    # Format du timestamp adapté pour Oracle
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")


    payload = {
        "image_base64": image_base64,
        "timestamp": timestamp  # Format correct
    }
    #print(f"Payload envoyé : {payload}")

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(POST_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print("Snapshot envoyé avec succès.")
        elif response.status_code == 500:
            print("Erreur 500 : Problème côté serveur.")
            print(f"Message : {response.text}")
        else:
            print(f"Erreur {response.status_code} : {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi : {e}")


# Fonction pour récupérer et afficher les snapshots depuis ORDS
def retrieve_snapshots():
    try:
        response = requests.get(GET_URL)
        if response.status_code == 200:
            snapshots = response.json()["items"]
            for snapshot in snapshots:
                print(f"Snapshot ID: {snapshot['id']}, Timestamp: {snapshot['ts']}")
                base64_image = snapshot["base64_image"]
                image_data = base64.b64decode(base64_image)

                # Afficher l'image
                image = Image.open(BytesIO(image_data))
                image.show()
        else:
            print(f"Erreur lors de la récupération : {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération : {e}")

# Fonction principale
def main():
    print("Récupération des 10 lignes aléatoires...")
    data = fetch_random_10()

    if not data:
        print("Impossible de récupérer des données.")
        return

    print("\nAffichage et sauvegarde du graphique...")
    filename = "snapshot.png"
    plot_data_and_save(data, filename)

    print("\nEncodage de l'image et envoi à la base de données...")
    encoded_image = encode_image_to_base64(filename)
    send_snapshot_to_db(encoded_image)

    print("\nRécupération des snapshots depuis la base de données...")
    retrieve_snapshots()

if __name__ == "__main__":
    main()
