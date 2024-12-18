import base64
from PIL import Image


def normalize(values):
    min_val = min(values)
    max_val = max(values)
    if max_val - min_val == 0:
        return [0.5 for _ in values]
    return [(v - min_val) / (max_val - min_val) for v in values]


def save_and_encode_snapshot(fig, filename="snapshot.jpg", resize_width=500, resize_height=250, quality=60):
    fig.savefig("temp_snapshot.png")
    with Image.open("temp_snapshot.png") as img:
        img = img.resize((resize_width, resize_height))
        img = img.convert("RGB")
        img.save(filename, "JPEG", optimize=True, quality=quality)

    with open(filename, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
