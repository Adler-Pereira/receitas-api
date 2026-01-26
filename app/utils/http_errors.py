HTTP_ERRORS = {
    400: "Requisição inválida",
    401: "Acesso não autorizado",
    403: "Acesso negado",
    404: "Nenhuma receita encontrada",
    500: "Erro interno do servidor",
    502: "Resposta inválida da API externa",
    503: "Serviço indisponível",
}

def get_http_error(status_code: int) -> str:
    return HTTP_ERRORS.get(status_code, "Erro HTTP")
