import base64
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import normalize, save_and_encode_snapshot
from rest_api import fetch_random_10, send_snapshot_to_db, retrieve_snapshots
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

def create_gui():
    root = tk.Tk()
    root.title("Interface graphique - Instantané")

    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax2 = ax1.twinx()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    def refresh_graph():
        data = fetch_random_10()
        if not data:
            return
        ax1.clear()
        ax2.clear()
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
        ax2.plot(seconds, oli_normalized, label="OLI (normalisé)", marker="^", linestyle="-", color="green")

        ax1.set_title("Évolution des indicateurs sur 10 secondes")
        ax1.set_xlabel("Temps (secondes)")
        ax1.set_ylabel("Valeurs normalisées (OTI, WTI, ATI)")
        ax2.set_ylabel("Valeurs normalisées (OLI)")
        fig.tight_layout()
        canvas.draw()

    def take_snapshot():
        encoded_image = save_and_encode_snapshot(fig)
        send_snapshot_to_db(encoded_image)

    def view_snapshots():
        snapshots = retrieve_snapshots()
        for snapshot in snapshots:
            base64_image = snapshot["base64_image"]
            image_data = base64.b64decode(base64_image)
            image = Image.open(BytesIO(image_data))
            image.show()

    # Boutons
    button_frame = tk.Frame(root)
    button_frame.pack()

    tk.Button(button_frame, text="Afficher Graphique", command=refresh_graph).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Prendre et Envoyer un instantané", command=take_snapshot).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Récupérer Snapshots", command=view_snapshots).grid(row=0, column=2, padx=5, pady=5)

    root.mainloop()
