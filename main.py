from fastapi import FastAPI, Query
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Chilink activa"}

@app.get("/parser")
def parse_product(url: str = Query(...)):
    print(f"\n➡️ URL recibida: {url}\n")  # Debug para ver si llega el link

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
    except Exception as e:
        return {"error": f"No se pudo acceder a la página: {str(e)}"}

    if "falabella.cl" in url or "falabella.com" in url:
        try:
            title_tag = soup.find("h1", class_="fb-product-hero__title")
            price_tag = soup.select_one("span.fb-price__sale")
            image_tag = soup.find("img", class_="fb-image-viewer__image")

            if not title_tag or not price_tag or not image_tag:
                return {"error": "No se pudo extraer el nombre, precio o imagen"}

            title = title_tag.text.strip()
            price = price_tag.text.strip()
            image = image_tag["src"]

            return {
                "store": "Falabella",
                "title": title,
                "price": price,
                "image": image
            }
        except Exception as e:
            return {"error": f"No se pudo procesar el producto: {str(e)}"}

    return {"error": "Tienda no soportada"}
