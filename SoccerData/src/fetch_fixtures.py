"""
fetch_fixtures.py

- Descarga fixtures de la Primera División de Costa Rica (season 2024)
- Guarda un CSV en /data para reutilizarlo en análisis sin gastar requests
"""

from api_client import api_get
import pandas as pd
import os

# ==============================
# CONFIGURACIÓN
# ==============================
LEAGUE_ID = 162
SEASON = 2024

def main():
    print(">>> Descargando fixtures...")

# ==============================
# LLAMADA A LA API
# ==============================
    data = api_get(
        "/fixtures",
        params={
            "league": LEAGUE_ID,
            "season": SEASON,
            "timezone": "America/Costa_Rica",
        }
    )

    fixtures = data.get("response", [])
    print(f">>> Total partidos encontrados: {len(fixtures)}")

# ==============================
# PROCESAMIENTO DE DATOS
# ==============================
    rows = []
    for match in fixtures:
        fixture = match["fixture"]
        teams = match["teams"]
        goals = match["goals"]

        rows.append({
            "match_id": fixture["id"],
            "date": fixture["date"],
            "home_team": teams["home"]["name"],
            "away_team": teams["away"]["name"],
            "home_goals": goals["home"],
            "away_goals": goals["away"],
            "status": fixture["status"]["short"],
            "round": match["league"]["round"],
        })

    df = pd.DataFrame(rows)
    # ==============================
    # CREAR CARPETA DATA SI NO EXISTE
    # ==============================
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Guardamos archivo CSV
    output_path = "data/primera_division_2024_fixtures.csv"
    df.to_csv(output_path, index=False)

    print(">>> CSV guardado en:", output_path)
    print(df.head())

if __name__ == "__main__":
    main()