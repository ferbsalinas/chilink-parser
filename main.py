from fastapi import FastAPI, Query
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Chilink activa"}

@app.get("/parser")
def parse_product(url: str = Query(...)):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    if "falabella.cl" in url:
        try:
            title = soup.find("h1", class_="fb-product-hero__title").text.strip()
            price = soup.select_one("span.fb-price__sale").text.strip()
            return {"store": "Falabella", "title": title, "price": price}
        except:
            return {"error": "No se pudo extraer el producto"}

    return {"error": "Tienda no soportada"}
