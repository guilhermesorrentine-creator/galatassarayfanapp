# tabela.py (FINAL)

import requests

API_KEY = "7a77f57f6720931f9e0431758c92aafe"

HEADERS = {"x-apisports-key": API_KEY}

DEFAULT_LEAGUE_ID = 203  # Süper Lig
DEFAULT_SEASON = 2022    # <-- CORREÇÃO: Temporada 2022/2023
TEAM_ID = 645

def tabela(league_id=DEFAULT_LEAGUE_ID, season=DEFAULT_SEASON):
    url = f"https://v3.football.api-sports.io/standings?league={DEFAULT_LEAGUE_ID}&season={2022}"
    
    fallback_tabela = [
        {
            "rank": 0, 
            "team": {"name": "Dados da Tabela Indisponíveis", "id": TEAM_ID}, 
            "points": 0
        }
    ]

    try:
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        data = r.json()

        response = data.get("response")
        if response and len(response) > 0:
            league_data = response[0].get("league")
            if league_data:
                standings = league_data.get("standings")
                if standings and len(standings) > 0:
                    # A API retorna as classificações dentro de uma lista aninhada (standings[0])
                    return standings[0]

        return fallback_tabela

    except requests.exceptions.RequestException:
        return fallback_tabela
    except (KeyError, IndexError):
        return fallback_tabela