from json import JSONDecodeError
from fastapi import FastAPI, HTTPException
import requests
from deep_translator import GoogleTranslator

app = FastAPI()

translator_pt = GoogleTranslator(source="en", target="pt")
translator_en = GoogleTranslator(source="pt", target="en")

def get_HTTPError(stts_code: int) -> str:
    HTTP_ERRORS = {
        400: "Requisição inválida",
        401: "Acesso não autorizado",
        403: "Acesso negado",
        404: "Nenhuma receita encontrada",
        500: "Erro interno do servidor",
        502: "Bad Gateway",
        503: "Serviço indisponível",
    }
    return HTTP_ERRORS.get(stts_code, "Erro HTTP")

def trans_text(text: str) -> str:
    return translator_en.translate(text)

def trans_dict(data: dict) -> dict:
    meals = data.get("meals", [])
    FIELDS_TO_SKIP_TRANSLATE = {
        "idMeal",
        "strMealThumb",
        "strYoutube",
        "strSource",
        "strImageSource",
        "dateModified"
    }
    for meal in meals:
        for key, value in meal.items():
            if key not in FIELDS_TO_SKIP_TRANSLATE and isinstance(value, str) and value.strip():
                try:
                    meal[key] = translator_pt.translate(value)
                except Exception:
                    meal[key] = value
    return {
        "meals": meals
    }

@app.get("/recipe")
def get_receita(ingredient: str) -> dict:
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    ing_trans = trans_text(ingredient)
    params = {"s": ing_trans}
    HEADERS = {
        "User-Agent": "receitas-api-python",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            url,
            params = params,
            headers = HEADERS,
            timeout = 5
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("meals", []):
            raise HTTPException(
                status_code = 404,
                detail = "Nenhuma receita encontrada"
            )
        
        return trans_dict(data)

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        error = get_HTTPError(status_code)

        raise HTTPException(
            status_code = status_code,
            detail = error
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code = 504,
            detail = "Timeout ao se comunicar com a API de receitas"
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code = 503,
            detail = "Falha de conexão com a API de receitas"
        )

    except requests.exceptions.TooManyRedirects:
        raise HTTPException(
            status_code = 502,
            detail = "Erro de redirecionamento na API de receitas"
        )

    except requests.exceptions.InvalidURL:
        raise HTTPException(
            status_code = 400,
            detail = "URL da API de receitas inválida"
        )

    except (JSONDecodeError, ValueError):
        raise HTTPException(
            status_code = 502,
            detail = "Resposta inválida da API de receitas"
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code = 500,
            detail = f"Erro inesperado ao consumir API externa: {str(e)}"
        )
