from fastapi import FastAPI, Query
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Chilink activa"}

@app.get("/parser")
def parse_product(url: str = Query(...)):
    print(f"\n➡️ URL recibida: {url}\n")  # Debug para verificar la URL que llega

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
            title = soup.find("h1", class_="fb-product-hero__title").text.strip()
            price = soup.select_one("span.fb-price__sale").text.strip()
            return {
                "store": "Falabella",
                "title": title,
                "price": price
            }
        except Exception as e:
            return {"error": f"No se pudo extraer el producto: {str(e)}"}

    return {"error": "Tienda no soportada"}
