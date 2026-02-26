"""
analyze_fixtures.py

Radiografía estadística Primera División Costa Rica 2024

Este script:
- Lee el CSV descargado
- Filtra partidos finalizados
- Calcula métricas tipo análisis profesional
- Genera un gráfico listo para publicar (con insight en tarjeta)
"""

import pandas as pd
import matplotlib.pyplot as plt
import textwrap

CSV_PATH = "data/primera_division_2024_fixtures.csv"

print(">>> Cargando datos...")
df = pd.read_csv(CSV_PATH)

# Aseguramos tipo numérico
df["home_goals"] = pd.to_numeric(df["home_goals"], errors="coerce")
df["away_goals"] = pd.to_numeric(df["away_goals"], errors="coerce")

# Filtrar solo partidos finalizados
df = df[df["status"] == "FT"].copy()

print(">>> Partidos analizados:", len(df))

# ==========================
# MÉTRICAS BASE
# ==========================

df["total_goals"] = df["home_goals"] + df["away_goals"]

avg_goals = df["total_goals"].mean()

home_wins = (df["home_goals"] > df["away_goals"]).sum()
away_wins = (df["away_goals"] > df["home_goals"]).sum()
draws = (df["home_goals"] == df["away_goals"]).sum()

total_matches = len(df) if len(df) else 1  # evita división por cero

home_pct = home_wins / total_matches * 100
away_pct = away_wins / total_matches * 100
draw_pct = draws / total_matches * 100

# Overs
over_25 = (df["total_goals"] > 2.5).sum()
over_35 = (df["total_goals"] > 3.5).sum()

over25_pct = over_25 / total_matches * 100
over35_pct = over_35 / total_matches * 100

# ==========================
# RESULTADOS (CONSOLA)
# ==========================

print("\n📊 RADIOGRAFÍA LIGA PROMERICA 2024")
print("-" * 40)

print(f"⚽ Promedio de goles por partido: {avg_goals:.2f}")

print("\n🏠 Resultados:")
print(f"Victorias local: {home_wins} ({home_pct:.1f}%)")
print(f"Victorias visitante: {away_wins} ({away_pct:.1f}%)")
print(f"Empates: {draws} ({draw_pct:.1f}%)")

print("\n🔥 Tendencia de goles:")
print(f"Partidos Over 2.5 goles: {over_25} ({over25_pct:.1f}%)")
print(f"Partidos Over 3.5 goles: {over_35} ({over35_pct:.1f}%)")

print("\n>>> FIN DEL ANALISIS\n")

# ==========================
# GRÁFICO PERSONALIZADO PRO
# ==========================

labels = ["Local", "Empate", "Visitante"]
values = [home_wins, draws, away_wins]
percentages = [home_pct, draw_pct, away_pct]

# Tus colores (se quedan)
colors = ["#1B4332", "#3A5A40", "#344E41"]

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(labels, values, color=colors)

# Título
ax.set_title(
    "Radiografía de Resultados\nLiga Promerica 2024",
    fontsize=16,
    fontweight="bold",
    fontname="DejaVu Sans",
    pad=16
)

ax.set_ylabel("Cantidad de Partidos", fontsize=11)

# Limpieza de bordes
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Etiquetas con cantidad + porcentaje
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 3,
        f"{int(height)}\n({percentages[i]:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

# ==========================
# INSIGHT EN TARJETA ABAJO
# ==========================

# Más espacio inferior para que no choque con el eje X
fig.subplots_adjust(top=0.82, bottom=0.25)

insight_text = (
    f"Insight: La ventaja local es moderada ({home_pct:.1f}%)." + 
    "La localía influye, pero no domina. La Liga Promerica 2024 muestra equilibrio competitivo real."
)

wrapped = "\n".join(textwrap.wrap(insight_text, width=60))

fig.text(
    0.5, 0.06,
    wrapped,
    ha="center",
    va="center",
    fontsize=11,
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#D9D9D9")
)

# Subtítulo pro (n + promedio)
fig.text(
    0.5, 0.15,
    f"Partidos analizados: {total_matches} | Promedio de goles: {avg_goals:.2f}",
    ha="center",
    fontsize=10
)

fig.text(
    0.99, 0.01,
    "Fuente: API-Football | Season 2024",
    ha="right",
    fontsize=8,
    color="gray"
)

# Guardar en alta calidad
plt.savefig("data/resultados_2024_custom.png", dpi=300, bbox_inches="tight")
plt.show()