import requests
import base64
import datetime
from tkinter import messagebox

# URLs des endpoints REST
URL = "http://localhost:8080/ords/hr/projet/projet_internal_random"
POST_URL = "http://localhost:8080/ords/hr/snapshots/upload"
GET_URL = "http://localhost:8080/ords/hr/snapshots/retrieve"

def fetch_random_10():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data["items"]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur", f"Erreur lors de la requête : {e}")
        return []

def send_snapshot_to_db(encoded_image):
    payload = {
        "image_base64": encoded_image,
        "timestamp": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(POST_URL, json=payload, headers=headers)
        if response.status_code == 200:
            messagebox.showinfo("Succès", "Snapshot envoyé avec succès.")
        else:
            messagebox.showerror("Erreur", f"Erreur lors de l'envoi : {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'envoi : {e}")

def retrieve_snapshots():
    try:
        response = requests.get(GET_URL)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération : {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur", f"Erreur lors de la récupération : {e}")
        return []
