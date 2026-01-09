import requests
import random

API_KEY = "7a77f57f6720931f9e0431758c92aafe"

HEADERS = {
    "x-apisports-key": API_KEY
}

TEAM_ID = 645
SEASON = 2022 # <-- CORREÇÃO: Temporada 2022/2023 consolidada


def jogadores():
    url = f"https://v3.football.api-sports.io/players?team={645}&season={2022}"
    status_opcoes = ["Disponível", "Dúvida", "Indisponível"]
    lista = []
    
    # Dados de Fallback (para quando a API falhar completamente)
    fallback_jogador = {
        "nome": "Jogador Indisponível",
        "posicao": "N/A",
        "foto": "N/A", 
        "status": "Indisponível"
    }

    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        for item in data.get("response", [])[:25]:
            player = item["player"]
            
            # CORREÇÃO CRÍTICA: Verifica se 'statistics' existe e não está vazia
            statistics = item.get("statistics")
            if statistics and len(statistics) > 0:
                stats = statistics[0]
                lista.append({
                    "nome": player["name"],
                    "posicao": stats["games"]["position"],
                    "foto": player["photo"],
                    "status": random.choice(status_opcoes)
                })
            else:
                # Adiciona o jogador com dados de fallback se as estatísticas falharem
                lista.append({
                    "nome": player["name"],
                    "posicao": "Sem Posição",
                    "foto": player["photo"],
                    "status": "Dúvida"
                })

    except requests.exceptions.RequestException as e:
        print(f"ERRO DE REQUISIÇÃO (jogadores.py): {e}")
    except KeyError as e:
        print(f"ERRO DE DADOS (jogadores.py): Chave faltando: {e}")

    # Garante que a lista não esteja vazia, senão o main.py pode falhar ao renderizar a lista
    if not lista:
        lista.append(fallback_jogador)
        
    return lista