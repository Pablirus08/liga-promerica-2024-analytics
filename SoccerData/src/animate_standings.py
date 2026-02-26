"""
animate_standings.py

Animación fluida: evolución de tabla por jornada (round).
Mejoras:
1) Color fijo por equipo.
2) Animación más fluida usando interpolación entre rondas.
3) Filtro opcional para solo Clausura (por texto o por fechas).

Requisitos:
  python -m pip install matplotlib pandas pillow
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

CSV_PATH = "data/primera_division_2024_fixtures.csv"
OUT_GIF = "data/tabla_clausura_2024_animada.gif"

TOP_N = 12
INTERP_STEPS = 8      # más = más fluido (6-12 recomendado)
INTERVAL_MS = 120     # menor = más fluido (80-150 recomendado)

# =============== FILTRO TORNEO ===============
USE_CLAUSURA_FILTER = True

# Opción A (recomendada): filtrar por palabra en round
CLAUSURA_KEYWORD = "Clausura"

# Opción B: filtrar por fechas (si round no trae Clausura)
USE_DATE_FILTER = False
DATE_FROM = "2024-01-01"
DATE_TO   = "2024-06-30"
# ===========================================


def points(home_goals, away_goals, side):
    if home_goals == away_goals:
        return 1
    if side == "home":
        return 3 if home_goals > away_goals else 0
    return 3 if away_goals > home_goals else 0


def build_table_snapshot(df, teams):
    table = pd.DataFrame({
        "team": teams,
        "MP": 0, "W": 0, "D": 0, "L": 0,
        "GF": 0, "GA": 0, "GD": 0,
        "PTS": 0
    }).set_index("team")
    return table


def apply_matches_to_table(table, matches):
    for m in matches.itertuples():
        ht, at = m.home_team, m.away_team
        hg, ag = int(m.home_goals), int(m.away_goals)

        table.loc[ht, "MP"] += 1
        table.loc[at, "MP"] += 1

        table.loc[ht, "GF"] += hg
        table.loc[ht, "GA"] += ag
        table.loc[at, "GF"] += ag
        table.loc[at, "GA"] += hg

        if hg > ag:
            table.loc[ht, "W"] += 1
            table.loc[at, "L"] += 1
        elif hg < ag:
            table.loc[at, "W"] += 1
            table.loc[ht, "L"] += 1
        else:
            table.loc[ht, "D"] += 1
            table.loc[at, "D"] += 1

        table.loc[ht, "PTS"] += points(hg, ag, "home")
        table.loc[at, "PTS"] += points(hg, ag, "away")

    table["GD"] = table["GF"] - table["GA"]


def sort_table(table):
    snap = table.reset_index().copy()
    snap = snap.sort_values(["PTS", "GD", "GF"], ascending=[False, False, False])
    return snap


def interpolate_frames(prev_snap, next_snap, round_label, steps):
    """
    Crea frames intermedios interpolando PTS (y opcionalmente GD, GF).
    Esto da sensación de movimiento suave.
    """
    # aseguramos mismo set de equipos
    prev = prev_snap.set_index("team")
    nxt = next_snap.set_index("team")

    teams = prev.index.union(nxt.index)

    prev = prev.reindex(teams).fillna(0)
    nxt = nxt.reindex(teams).fillna(0)

    frames = []
    for s in range(steps):
        t = (s + 1) / steps
        cur = prev.copy()
        # interpolamos puntos
        cur["PTS"] = prev["PTS"] + (nxt["PTS"] - prev["PTS"]) * t
        cur["GD"]  = prev["GD"]  + (nxt["GD"]  - prev["GD"])  * t
        cur["GF"]  = prev["GF"]  + (nxt["GF"]  - prev["GF"])  * t

        cur = cur.reset_index()
        cur["round"] = round_label
        cur = cur.sort_values(["PTS", "GD", "GF"], ascending=[False, False, False])

        frames.append(cur)

    return frames


def make_team_colors(teams):
    """
    Colores personalizados por equipo (aproximados a sus colores reales).
    """

    team_palette = {
        "LD Alajuelense": "#5C0B0E",      # Rojinegro
        "Deportivo Saprissa": "#32032B",  # Morado
        "CS Herediano": "#DB7F05",        # Amarillo
        "CS Cartagines": "#062B79",       # Azul
        "San Carlos": "#F23A3A",          # Azul fuerte
        "AD Guanacasteca": "#055C29",     # Verde
        "Santos DE Guapiles": "#D37075",  # Negro/gris oscuro
        "Santa Ana": "#344658",           # Gris claro
        "Puntarenas FC": "#CA3005",       # Naranja
        "Perez Zeledon": "#06399E",       # Azul claro
        "Sporting San Jose": "#222222",   # Gris
    }

    colors = {}
    for team in teams:
        colors[team] = team_palette.get(team, "#7F8C8D")  # gris si no está definido

    return colors


def main():
    df = pd.read_csv(CSV_PATH)

    # Solo FT
    df = df[df["status"] == "FT"].copy()

    # Parse date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "round"])

    # Goles
    df["home_goals"] = pd.to_numeric(df["home_goals"], errors="coerce")
    df["away_goals"] = pd.to_numeric(df["away_goals"], errors="coerce")
    df = df.dropna(subset=["home_goals", "away_goals"])

    # --------- FILTRO TORNEO DE CLAUSURA ----------
    if USE_CLAUSURA_FILTER:
        if CLAUSURA_KEYWORD:
            df = df[df["round"].astype(str).str.contains(CLAUSURA_KEYWORD, case=False, na=False)].copy()

    if USE_DATE_FILTER:
        dfrom = pd.to_datetime(DATE_FROM)
        dto = pd.to_datetime(DATE_TO)
        df = df[(df["date"] >= dfrom) & (df["date"] <= dto)].copy()
    # -------------------------------------------

    if df.empty:
        raise RuntimeError("El DataFrame quedó vacío. Ajusta el filtro Clausura (keyword o fechas).")

    # Orden cronológico
    df = df.sort_values("date")

    teams = pd.unique(df[["home_team", "away_team"]].values.ravel())
    team_colors = make_team_colors(teams)

    # Rounds en orden de aparición cronológica
    rounds = df["round"].dropna().unique().tolist()
    print(">>> Rounds encontrados:", len(rounds))
    print(">>> Ejemplo round:", rounds[0])

    # Construimos snapshots por round
    table = build_table_snapshot(df, teams)
    snaps = []

    for r in rounds:
        matches = df[df["round"] == r]
        apply_matches_to_table(table, matches)
        snap = sort_table(table)
        snap["round"] = r
        snaps.append(snap)

    # Crear frames interpolados para suavidad
    frames = []
    frames.append(snaps[0])  # primer frame
    for i in range(1, len(snaps)):
        frames.extend(interpolate_frames(snaps[i-1], snaps[i], snaps[i]["round"].iloc[0], INTERP_STEPS))

    print(">>> Frames totales (con interpolación):", len(frames))

    # ===== ANIMACIÓN =====
    fig, ax = plt.subplots(figsize=(11, 6))

    def draw(frame_idx):
        ax.clear()
        snap = frames[frame_idx].head(TOP_N).copy()

        # para que el líder quede arriba
        snap = snap.iloc[::-1]

        bar_colors = [team_colors[t] for t in snap["team"]]

        ax.barh(snap["team"], snap["PTS"], color=bar_colors)

        # título dinámico
        rlabel = snap["round"].iloc[0]
        ax.set_title(f"Evolución de la tabla (PTS)\n{rlabel}", fontsize=16, fontweight="bold", pad=18)
        ax.set_xlabel("Puntos (PTS)")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", linestyle="--", alpha=0.25)

        # etiquetas puntos
        for i, (team, pts) in enumerate(zip(snap["team"], snap["PTS"])):
            ax.text(float(pts) + 0.15, i, f"{int(round(float(pts)))}", va="center", fontsize=10, fontweight="bold")

        fig.text(0.99, 0.01, "Fuente: API-Football | Season 2024", ha="right", fontsize=8, color="gray")

    ani = animation.FuncAnimation(
        fig,
        draw,
        frames=len(frames),
        interval=INTERVAL_MS,
        repeat=False
    )

    ani.save(OUT_GIF, writer="pillow", dpi=140)
    plt.close(fig)

    print(f">>> GIF guardado en: {OUT_GIF}")


if __name__ == "__main__":
    main()