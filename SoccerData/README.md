# 🇨🇷 Liga Promerica 2024 – Sports Analytics Project

Proyecto de análisis exploratorio de datos de la Primera División de Costa Rica (Liga Promerica 2024) utilizando Python y datos obtenidos desde API-Football.

El objetivo del proyecto es analizar tendencias estructurales del torneo y construir visualizaciones profesionales que permitan entender el comportamiento competitivo de la liga.

---

## 📊 Análisis Realizados

### 1️⃣ Radiografía General de Liga
- Promedio de goles por partido
- Distribución de victorias (local vs visitante)
- Tendencias de Over 2.5 y Over 3.5 goles

📌 Insight principal:
La liga muestra una ventaja local moderada (≈45%) y un equilibrio competitivo significativo.

---

### 2️⃣ Top 5 Ataques – Goles vs Diferencia de Gol
- Comparación entre goles anotados y diferencia de gol.
- Identificación de eficiencia estructural (ataque + defensa).

📌 Insight principal:
Algunos equipos no lideran en goles anotados, pero sí en diferencia de gol, reflejando mayor eficiencia competitiva.

---

### 3️⃣ Dependencia de Localía (PPG Gap)
- Cálculo de puntos por partido (PPG) como local y visitante.
- Medición del gap entre rendimiento en casa vs fuera.

📌 Insight principal:
Se identificaron equipos con alta dependencia de localía, evidenciando caída significativa de rendimiento fuera de casa.

---

### 4️⃣ 🎥 Evolución de la Tabla – Clausura 2024
Animación tipo "bar chart race" mostrando cómo se movió la tabla jornada a jornada durante el torneo Clausura 2024.

- Tabla acumulada por puntos.
- Orden dinámico por PTS, diferencia de gol y goles a favor.
- Colores personalizados por equipo.
- Animación fluida mediante interpolación entre jornadas.

---

## 🛠️ Tecnologías Utilizadas

- Python 3.14
- Pandas
- Matplotlib
- Pillow (animaciones)
- API-Football

## 📂 Estructura del Proyecto
SoccerData/
│
├── src/
│   ├── api_client.py
│   ├── analyze_fixtures.py
│   ├── analyze_teams.py
│   ├── analyze_home_away.py
│   ├── animate_standings.py
│
├── data/
│   ├── primera_division_2024_fixtures.csv
│   ├── resultados_2024.png
│   ├── top5_gf_vs_dg_2024.png
│   ├── home_vs_away_ppg_gap_2024.png
│   ├── tabla_clausura_2024_animada.gif
│
├── requirements.txt
├── .gitignore
├── README.md

## 🔐 Notas Importantes

La API key no está incluida por motivos de seguridad.

El archivo .env no se sube al repositorio.

El entorno virtual (venv/) está excluido mediante .gitignore.

## 🎯 Objetivo del Proyecto

Este proyecto busca demostrar:

- Capacidad de análisis exploratorio en contexto deportivo
- Construcción de métricas competitivas relevantes
- Generación de visualizaciones profesionales
- Estructuración adecuada de un proyecto reproducible en Python

## 📈 Posibles Extensiones Futuras

Expected Goals (xG) analysis
Índice compuesto de rendimiento (ataque + defensa + localía)
Dashboard interactivo (Streamlit o Power BI)
Comparación Apertura vs Clausura
Modelado predictivo básico

## 📎 Fuente de Datos

Datos obtenidos mediante API-Football.
URL: https://www.api-football.com/

## 👤 Autor
Pablo Elmer P.
Proyecto desarrollado como parte de un portafolio de Sports & Data Analytics.