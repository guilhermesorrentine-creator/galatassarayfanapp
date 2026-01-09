import requests

API_KEY = "7a77f57f6720931f9e0431758c92aafe"

HEADERS = {
    "x-apisports-key": API_KEY
}

def dados_clube():
    url = "https://v3.football.api-sports.io/teams?id=645"
    
    # Dados de Fallback (Retorno seguro)
    fallback_data = {
        "nome": "Galatasaray (Dados Indisponíveis)",
        "fundacao": "N/A",
        "pais": "N/A",
        "logo": "N/A",
        "estadio": "N/A",
        "capacidade": "N/A"
    }

    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status() # Lança exceção para erros HTTP
        data_json = r.json()

        # CORREÇÃO: Verifica se 'response' existe e tem dados antes de acessar [0]
        if data_json.get("response") and len(data_json["response"]) > 0:
            data = data_json["response"][0]
            return {
                "nome": data["team"]["name"],
                "fundacao": data["team"]["founded"],
                "pais": data["team"]["country"],
                "logo": data["team"]["logo"],
                "estadio": data["venue"]["name"],
                "capacidade": data["venue"]["capacity"]
            }
        else:
            print("AVISO (clube.py): Dados do clube não encontrados na API.")
            return fallback_data
    
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE REQUISIÇÃO (clube.py): {e}")
        return fallback_data
    except (KeyError, IndexError) as e:
        print(f"ERRO DE DADOS (clube.py): Estrutura JSON inesperada. Chave/Índice: {e}")
        return fallback_data