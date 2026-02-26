"""
analyze_teams.py

Análisis por equipos Primera División Costa Rica 2024

Este script:
- Lee el CSV de fixtures
- Calcula estadísticas por equipo
- Genera ranking ofensivo
"""

import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "data/primera_division_2024_fixtures.csv"

print(">>> Cargando datos...")
df = pd.read_csv(CSV_PATH)

# Filtrar partidos finalizados
df = df[df["status"] == "FT"].copy()

# ==========================
# CONSTRUIR TABLA POR EQUIPO
# ==========================

teams_data = []

teams = pd.unique(df[["home_team", "away_team"]].values.ravel())

for team in teams:

    home_games = df[df["home_team"] == team]
    away_games = df[df["away_team"] == team]

    goals_for = home_games["home_goals"].sum() + away_games["away_goals"].sum()
    goals_against = home_games["away_goals"].sum() + away_games["home_goals"].sum()

    matches_played = len(home_games) + len(away_games)

    teams_data.append({
        "team": team,
        "matches": matches_played,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "goal_diff": goals_for - goals_against,
        "goals_per_match": goals_for / matches_played if matches_played > 0 else 0
    })

teams_df = pd.DataFrame(teams_data)

# Ordenar por mejor ataque
teams_df = teams_df.sort_values(by="goals_for", ascending=False)

print("\n📊 TOP 5 ATAQUES 2024")
print(teams_df.head())

# ==========================
# GRÁFICO: GOLES VS DIFERENCIA DE GOL (TOP 5)
# ==========================

top5 = teams_df.head(5).copy()

team_colors = {
    "CS Herediano": "#1B4332",
    "Deportivo Saprissa": "#3A5A40",
    "LD Alajuelense": "#344E41",
    "CS Cartagines": "#2D6A4F",
    "San Carlos": "#40916C",
}

colors = [team_colors.get(t, "#1B4332") for t in top5["team"]]

fig, ax = plt.subplots(figsize=(10, 6))

scatter = ax.scatter(
    top5["goals_for"],
    top5["goal_diff"],
    s=220,
    c=colors,
    edgecolors="black",
    linewidths=1
)

# Título más equilibrado
ax.set_title(
    "Goles Anotados vs Diferencia de Gol\nLiga Promerica 2024 – Top 5",
    fontsize=15,
    fontweight="bold",
    pad=20
)

ax.set_xlabel("Goles anotados (GF)", fontsize=12)
ax.set_ylabel("Diferencia de gol (DG)", fontsize=12)

# Líneas guía suaves
ax.grid(axis="y", linestyle="--", alpha=0.3)

# Quitar bordes innecesarios
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Ajustar límites para dar aire
ax.set_xlim(top5["goals_for"].min() - 2, top5["goals_for"].max() + 3)
ax.set_ylim(top5["goal_diff"].min() - 3, top5["goal_diff"].max() + 3)

# Etiquetas mejor posicionadas
for _, row in top5.iterrows():

    x = row["goals_for"]
    y = row["goal_diff"]

    ax.annotate(
        f"{row['team']}\nGF:{int(x)} | DG:{int(y)}",
        (x, y),
        textcoords="offset points",
        xytext=(8, 8),
        fontsize=9
    )

# Insight más compacto y profesional
insight = "Alajuelense no lidera en goles, pero sí en diferencia → eficiencia defensiva."

fig.subplots_adjust(bottom=0.20)

fig.text(
    0.5,
    0.12,
    insight,
    ha="center",
    fontsize=10,
    fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#678570")
)

# Footer profesional
fig.text(
    0.99,
    0.01,
    "Fuente: API-Football | Season 2024",
    ha="right",
    fontsize=8,
    color="gray"
)

plt.tight_layout()
plt.savefig("data/top5_gf_vs_dg_2024.png", dpi=300, bbox_inches="tight")
plt.show() 