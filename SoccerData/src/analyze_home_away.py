"""
analyze_home_away.py

Rendimiento Local vs Visitante – Primera División Costa Rica 2024

Este script:
- Lee el CSV de fixtures (FT)
- Calcula puntos y puntos por partido (PPG) como local y como visitante
- Genera un gráfico: Top 10 equipos con mayor diferencia (PPG Local - PPG Visita)
"""

import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "data/primera_division_2024_fixtures.csv"

print(">>> Cargando datos...")
df = pd.read_csv(CSV_PATH)

# Solo partidos finalizados
df = df[df["status"] == "FT"].copy()

# Asegurar numéricos
df["home_goals"] = pd.to_numeric(df["home_goals"], errors="coerce")
df["away_goals"] = pd.to_numeric(df["away_goals"], errors="coerce")

# -----------------------
# Funciones de puntos
# -----------------------
def points_for(home_goals, away_goals, side: str) -> int:
    """
    Retorna puntos del equipo según el lado:
    side='home' o side='away'
    """
    if pd.isna(home_goals) or pd.isna(away_goals):
        return 0

    if home_goals == away_goals:
        return 1

    if side == "home":
        return 3 if home_goals > away_goals else 0
    else:
        return 3 if away_goals > home_goals else 0


# -----------------------
# Construcción por equipo
# -----------------------
teams = pd.unique(df[["home_team", "away_team"]].values.ravel())
rows = []

for team in teams:
    home_games = df[df["home_team"] == team]
    away_games = df[df["away_team"] == team]

    home_points = sum(points_for(r.home_goals, r.away_goals, "home") for r in home_games.itertuples())
    away_points = sum(points_for(r.home_goals, r.away_goals, "away") for r in away_games.itertuples())

    home_matches = len(home_games)
    away_matches = len(away_games)

    home_ppg = home_points / home_matches if home_matches > 0 else 0
    away_ppg = away_points / away_matches if away_matches > 0 else 0

    rows.append({
        "team": team,
        "home_matches": home_matches,
        "away_matches": away_matches,
        "home_points": home_points,
        "away_points": away_points,
        "home_ppg": home_ppg,
        "away_ppg": away_ppg,
        "ppg_gap": home_ppg - away_ppg
    })

teams_df = pd.DataFrame(rows)

# Top 10 mayor diferencia (más dependientes del local)
top10 = teams_df.sort_values("ppg_gap", ascending=False).head(10).copy()

print("\n📊 TOP 10 EQUIPOS CON MAYOR GAP (PPG Local - PPG Visita)")
print(top10[["team", "home_ppg", "away_ppg", "ppg_gap"]])

# -----------------------
# Gráfico
# -----------------------
colors = ["#276048"] * len(top10)  # verde base de tu marca

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(top10["team"], top10["ppg_gap"], color=colors)

ax.set_title("Dependencia de Localía – Liga Promerica 2024\n(PPG Local - PPG Visita) | Top 10",
             fontsize=15, fontweight="bold", pad=20)
ax.set_xlabel("Diferencia de Puntos por Partido (PPG)")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="x", linestyle="--", alpha=0.3)

ax.invert_yaxis()

# Etiquetas al final de cada barra
for i, v in enumerate(top10["ppg_gap"]):
    ax.text(v + 0.02, i, f"{v:.2f}", va="center", fontsize=10, fontweight="bold")

# Insight (simple y publicable)
best_team = top10.iloc[0]["team"]
best_gap = top10.iloc[0]["ppg_gap"]

insight = f"Insight: {best_team} muestra la mayor dependencia de localía (gap {best_gap:.2f} PPG)."
fig.text(
    0.35, 0.13,
    insight,
    ha="left",
    fontsize=11,
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#CFCFCF")
)

fig.text(0.99, 0.01, "Fuente: API-Football | Season 2024", ha="right", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("data/home_vs_away_ppg_gap_2024.png", dpi=300, bbox_inches="tight")
plt.show()