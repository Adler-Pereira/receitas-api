from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/recipe")
def get_receita(ingredient: str) -> dict:
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    params = {"s": ingredient}
    headers = {
        "User-Agent": "receitas-api-python",
        "Accept": "application/json"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    data = response.json()

    if not data.get("meals"):
        return {
            "erro": "Nenhuma receita encontrada."
        }
        
    return data    
