from json import JSONDecodeError
from fastapi import FastAPI, HTTPException
import requests
from deep_translator import GoogleTranslator

app = FastAPI()

translator_pt = GoogleTranslator(source="en", target="pt")
translator_en = GoogleTranslator(source="pt", target="en")

def get_HTTPError(sts_code: int) -> str:
    match sts_code:
        case 400:
            error = "Requisição inválida"
        case 401:
            error = "Acesso não autorizado"
        case 403:
            error = "Acesso negado"
        case 404:
            error = "Nenhuma receita encontrada"
        case 500:
            error = "Erro interno do servidor"
        case 502:
            error = "Bad Gateway"
        case 503:
            error = "Serviço indisponível"
        case _:
            error = "Erro HTTP"
    return error

def trans_text(text: str) -> str:
    txt_trans = translator_en.translate(text)
    return txt_trans

def trans_dict(data: dict) -> dict:
    meals = data.get("meals", [])
    for meal in meals:
        for key, value in meal.items():
            if isinstance(value, str) and value.strip():
                translated = translator_pt.translate(value)
                meal[key] = translated
    return {
        "meals": meals
    }

@app.get("/recipe")
def get_receita(ingredient: str) -> dict:
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    ing_trans = trans_text(ingredient)
    params = {"s": ing_trans}
    headers = {
        "User-Agent": "receitas-api-python",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            url,
            params = params,
            headers = headers,
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
