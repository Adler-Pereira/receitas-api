from fastapi import FastAPI
from app.services.recipe_service import get_recipe_by_ingredient

app = FastAPI()


@app.get("/recipe")
def get_receita(ingredient: str) -> dict:
    return get_recipe_by_ingredient(ingredient)
