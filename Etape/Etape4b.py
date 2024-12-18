import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import requests
import datetime
import base64
from PIL import Image
from io import BytesIO

# URLs des endpoints REST
URL = "http://localhost:8080/ords/hr/projet/projet_internal_random"
POST_URL = "http://localhost:8080/ords/hr/snapshots/upload"
GET_URL = "http://localhost:8080/ords/hr/snapshots/retrieve"


# Fonction pour récupérer les 10 lignes aléatoires
def fetch_random_10():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data["items"]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur", f"Erreur lors de la requête : {e}")
        return []


# Fonction pour normaliser les données
def normalize(values):
    min_val = min(values)
    max_val = max(values)
    if max_val - min_val == 0:
        return [0.5 for _ in values]
    return [(v - min_val) / (max_val - min_val) for v in values]


# Fonction pour afficher et sauvegarder le graphique
def plot_data(data, fig, ax1, ax2):
    ax1.clear()
    ax2.clear()
    if not data:
        messagebox.showerror("Erreur", "Aucune donnée à afficher.")
        return

    seconds = list(range(10))
    oti = [d["oti"] for d in data]
    wti = [d["wti"] for d in data]
    oli = [d["oli"] for d in data]
    ati = [d["ati"] for d in data]

    oti_normalized = normalize(oti)
    wti_normalized = normalize(wti)
    oli_normalized = normalize(oli)
    ati_normalized = normalize(ati)

    ax1.plot(seconds, oti_normalized, label="OTI (normalisé)", marker="o", linestyle="--", color="blue")
    ax1.plot(seconds, wti_normalized, label="WTI (normalisé)", marker="s", linestyle="-.", color="orange")
    ax1.plot(seconds, ati_normalized, label="ATI (normalisé)", marker="x", linestyle=":", color="purple")
    ax1.set_xlabel("Temps (secondes)")
    ax1.set_ylabel("Valeurs normalisées (OTI, WTI, ATI)")

    ax2.plot(seconds, oli_normalized, label="OLI (normalisé)", marker="^", linestyle="-", color="green")
    ax2.set_ylabel("Valeurs normalisées (OLI)")

    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    ax1.set_title("Évolution des indicateurs sur 10 secondes")
    fig.tight_layout()


# Fonction pour sauvegarder l'instantané et l'envoyer au serveur
def save_and_send_snapshot(fig, resize_width=500, resize_height=250):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    png_filename = f"snapshot_{timestamp}.png"
    jpeg_filename = f"snapshot_{timestamp}.jpg"
    try:
        fig.savefig(png_filename)

        # Redimensionner l'image et convertir en JPEG
        with Image.open(png_filename) as img:
            img = img.resize((resize_width, resize_height))
            img = img.convert("RGB")
            img.save(jpeg_filename, "JPEG", optimize=True, quality=60)

        messagebox.showinfo("Succès", f"Instantané sauvegardé sous : {jpeg_filename}")

        # Encodage de l'image en Base64
        with open(jpeg_filename, "rb") as file:
            encoded_image = base64.b64encode(file.read()).decode("utf-8")

        # Envoi de l'image encodée au serveur
        payload = {
            "image_base64": encoded_image,
            "timestamp": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(POST_URL, json=payload, headers=headers)

        if response.status_code == 200:
            messagebox.showinfo("Succès", "Snapshot envoyé avec succès.")
        else:
            messagebox.showerror("Erreur", f"Erreur lors de l'envoi : {response.status_code} - {response.text}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde ou de l'envoi : {e}")


# Fonction pour récupérer et afficher les snapshots depuis le serveur
def retrieve_snapshots():
    try:
        response = requests.get(GET_URL)
        if response.status_code == 200:
            snapshots = response.json()["items"]
            for snapshot in snapshots:
                base64_image = snapshot["base64_image"]
                image_data = base64.b64decode(base64_image)
                image = Image.open(BytesIO(image_data))
                image.show()
        else:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération : {response.status_code} - {response.text}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération : {e}")


# Interface graphique principale
root = tk.Tk()
root.title("Interface graphique - Instantané")

fig, ax1 = plt.subplots(figsize=(6, 4))
ax2 = ax1.twinx()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()


def refresh_graph():
    data = fetch_random_10()
    plot_data(data, fig, ax1, ax2)
    canvas.draw()


# Boutons
button_frame = tk.Frame(root)
button_frame.pack()

refresh_button = tk.Button(button_frame, text="Afficher Graphique", command=refresh_graph)
refresh_button.grid(row=0, column=0, padx=5, pady=5)

snapshot_button = tk.Button(button_frame, text="Prendre et Envoyer un instantané",
                            command=lambda: save_and_send_snapshot(fig))
snapshot_button.grid(row=0, column=1, padx=5, pady=5)

retrieve_button = tk.Button(button_frame, text="Récupérer Snapshots", command=retrieve_snapshots)
retrieve_button.grid(row=0, column=2, padx=5, pady=5)

root.mainloop()
