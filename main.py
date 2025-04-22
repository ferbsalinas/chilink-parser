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
            title = soup.find("h1", class_="jsx-1289233143 product-name").text.strip()
            price = soup.find("span", class_="jsx-1289233143 copy10 primary medium line-height-24 normal breakword").text.strip()
            image = soup.find("img", class_="jsx-3974001354")["src"]

            return {
                "store": "Falabella",
                "title": title,
                "price": price,
                "image": image
            }
        except Exception as e:
            return {"error": f"No se pudo extraer el producto: {str(e)}"}

    return {"error": "Tienda no soportada"}
