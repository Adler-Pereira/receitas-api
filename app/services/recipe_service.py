import requests
from json import JSONDecodeError
from fastapi import HTTPException

from app.services.translation_service import (
    translate_text_to_en,
    translate_meals
)
from app.utils.http_errors import get_http_error

HEADERS = {
    "User-Agent": "receitas-api-python",
    "Accept": "application/json"
}

URL = "https://www.themealdb.com/api/json/v1/1/search.php"


def get_recipe_by_ingredient(ingredient: str) -> dict:
    ingredient_en = translate_text_to_en(ingredient)
    params = {"s": ingredient_en}

    try:
        response = requests.get(
            URL,
            params=params,
            headers=HEADERS,
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("meals"):
            raise HTTPException(404, "Nenhuma receita encontrada")

        return translate_meals(data)

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        raise HTTPException(
            status_code=status_code,
            detail=get_http_error(status_code)
        )

    except requests.exceptions.Timeout:
        raise HTTPException(504, "Timeout ao se comunicar com a API de receitas")

    except requests.exceptions.ConnectionError:
        raise HTTPException(503, "Falha de conexão com a API de receitas")

    except requests.exceptions.TooManyRedirects:
        raise HTTPException(502, "Erro de redirecionamento na API de receitas")

    except requests.exceptions.InvalidURL:
        raise HTTPException(400, "URL da API de receitas inválida")

    except (JSONDecodeError, ValueError):
        raise HTTPException(502, "Resposta inválida da API de receitas")

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            500,
            f"Erro inesperado ao consumir API externa: {str(e)}"
        )
