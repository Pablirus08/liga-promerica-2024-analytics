import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://v3.football.api-sports.io")
API_KEY = os.getenv("APISPORTS_KEY")

print(f">>> BASE_URL: {BASE_URL}")
print(f">>> APISPORTS_KEY cargada: {'SI' if API_KEY else 'NO'} | largo={len(API_KEY) if API_KEY else 0}")

if not API_KEY:
    raise RuntimeError("No se encontró APISPORTS_KEY en el .env (o el .env no se está cargando).")

HEADERS = {"x-apisports-key": API_KEY}

def api_get(endpoint: str, params: dict | None = None):
    url = f"{BASE_URL}{endpoint}"
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    print(f">>> GET {r.url} -> {r.status_code}")
    if r.status_code != 200:
        print(">>> Body:", r.text[:300])
    r.raise_for_status()
    return r.json()

