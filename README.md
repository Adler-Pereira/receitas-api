<h1 align="center" style="font-weight: bold;">🍽️ Receitas API (FastAPI)</h1>

<p align="center">
    <a href="#funcs">Funcionalidades</a> •
    <a href="#technologies">Tecnologias</a> •
    <a href="#started">Como Testar</a>
</p>

API REST desenvolvida em **Python + FastAPI** que consome a API pública **TheMealDB** para buscar receitas por ingrediente e retorna os dados **traduzidos automaticamente para português**, com foco em **boas práticas, tratamento robusto de erros e otimização de performance**.

---

<h2 id="funcs">🚀 Funcionalidades</h2>

* 🔍 Busca de receitas por ingrediente
* 🌐 Consumo de API externa (TheMealDB)
* 🌎 Tradução automática EN → PT usando `deep-translator`
* ⚡ Tradução em lote para melhor desempenho
* 🧠 Tratamento completo de erros HTTP e de rede
* 📦 Código organizado e legível

---

<h2 id="technologies">🛠️ Tecnologias Utilizadas</h2>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Uvicorn](https://img.shields.io/badge/Uvicorn-995591?style=for-the-badge&logo=uvicorn)
![Requests](https://img.shields.io/badge/Requests-505050?style=for-the-badge&logo=requests)
![Deep Translator (GoogleTranslator)](https://img.shields.io/badge/Deep_Translator_(GoogleTranslator)-995591?style=for-the-badge&logo=google)

---

## 📂 Estrutura do Projeto

```text
app/
 ├── main.py            # API FastAPI e rotas
 ├── venv/              # Ambiente virtual
 ├── requirements.txt   # Dependências do projeto
 ├── .gitignore         # Arquivos ignorados pelo Git
```

---

## 📌 Endpoint Disponível

### 🔹 Buscar receita por ingrediente

**GET** `/recipe`

#### Query Params

| Parâmetro  | Tipo   | Obrigatório | Descrição              |
| ---------- | ------ | ----------- | ---------------------- |
| ingredient | string | ✅           | Ingrediente para busca |

#### Exemplo de requisição

```http
GET /recipe?ingredient=chicken
```

---

## 📤 Exemplo de Resposta

```json
{
  "meals": [
    {
      "idMeal": "53005",
      "strMeal": "Torta De Morango E Ruibarbo",
      "strMealAlternate": null,
      "strCategory": "Sobremesa",
      "strArea": "Britânico",
      "strInstructions": "Massa de Torta: Em um processador...",
      "strMealThumb": "https://www.themealdb.com/images/media/meals/178z5o1585514569.jpg",
      "strTags": "Pudim, Torta, Assado, Frutado, Esmaltado",
      "strYoutube": "https://www.youtube.com/watch?v=tGw5Pwm4YA0",
      "strIngredient1": "Farinha",
      "strIngredient2": "Sal",
      "strIngredient3": "Açúcar",
      "strIngredient4": "Manteiga",
      "strIngredient5": "Água",
      "strIngredient6": "Ruibarbo",
      "strIngredient7": "Morangos",
      "strIngredient8": "Amido de milho",
      "strIngredient9": "Açúcar",
      "strIngredient10": "Canela",
      "strIngredient11": "Suco de Limão",
      "strIngredient12": "Manteiga sem sal",
      "strIngredient13": "Leite",
      "strIngredient14": "Açúcar",
      "strIngredient15": "",
      "strIngredient16": "",
      "strIngredient17": "",
      "strIngredient18": "",
      "strIngredient19": "",
      "strIngredient20": "",
      "strMeasure1": "350g",
      "strMeasure2": "1 colher de chá ",
      "strMeasure3": "2 colheres de sopa",
      "strMeasure4": "1 xícara ",
      "strMeasure5": "1/2 xícara ",
      "strMeasure6": "450g",
      "strMeasure7": "450g",
      "strMeasure8": "3 colheres de sopa",
      "strMeasure9": "150g",
      "strMeasure10": "1/4 colher de chá",
      "strMeasure11": "1 colher de chá ",
      "strMeasure12": "2 colheres de sopa",
      "strMeasure13": "2 colheres de sopa",
      "strMeasure14": "Cintilante",
      "strMeasure15": " ",
      "strMeasure16": " ",
      "strMeasure17": " ",
      "strMeasure18": " ",
      "strMeasure19": " ",
      "strMeasure20": " ",
      "strSource": "https://www.joyofbaking.com/StrawberryRhubarbPie.html",
      "strImageSource": null,
      "strCreativeCommonsConfirmed": null,
      "dateModified": null
    }
  ]
}
```

> ⚠️ Campos como URLs, IDs e datas **não são traduzidos**, apenas textos relevantes.

---

## ⚠️ Tratamento de Erros

A API retorna mensagens claras para os principais cenários:

| Status | Motivo                           |
| ------ | -------------------------------- |
| 400    | Requisição inválida              |
| 401    | Acesso não autorizado            |
| 403    | Acesso negado                    |
| 404    | Nenhuma receita encontrada       |
| 502    | Resposta inválida da API externa |
| 503    | Falha de conexão                 |
| 504    | Timeout                          |
| 500    | Erro inesperado                  |

---

## ⚡ Otimização de Performance

Para evitar múltiplas chamadas ao tradutor:

* Textos são **concatenados em um único payload**
* Um separador seguro é utilizado
* Tradução é feita **em lote**
* Limite de **4500 caracteres** para respeitar a API de tradução
* Fallback automático para tradução individual

---

<h2 id="started">▶️ Como Executar o Projeto</h2>

<h3>Pré-requisitos</h3>
- Python 3.12.10
<br>

### 1️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

### 2️⃣ Ativar ambiente virtual

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar o servidor

```bash
uvicorn app.main:app --reload
```

### 5️⃣ Acessar a documentação automática

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Conceitos Aplicados

* Clean Code
* Separation of Concerns
* Tratamento explícito de exceções
* Defensive programming
* Integração com APIs externas
* Performance em chamadas HTTP


---

## 👨‍💻 Autor

**Adler-Pereira**

Projeto desenvolvido com foco em aprendizado prático de backend Python, APIs REST e boas práticas profissionais
