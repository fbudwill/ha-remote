from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ─── Konfiguration ────────────────────────────────────────────────────────────
HA_URL = os.environ["HA_URL"]      # z.B. http://192.168.1.10:8123
HA_TOKEN = os.environ["HA_TOKEN"]  # Home Assistant Long-Lived Access Token

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# ─── Button-Definitionen ──────────────────────────────────────────────────────
# Jeder Button hat:
#   label     – Text auf dem Button
#   service   – HA-Service im Format "domain.service"
#   entity_id – Ziel-Entity (oder None bei Skripten/Szenen ohne explizite Entity)
#   group     – Gruppe für die Darstellung (frei wählbar)

# notify.alexa_media_kuche

BUTTONS = [
    {
        "label": "Toggle Schreibtisch",
        "service": "switch.toggle",
        "entity_id":"switch.smart_plug_mini",
        "group": "Schalter",
    },
    {
        "label": "Toggle Wohnzimmer",
        "service": "switch.toggle",
        "entity_id":"switch.smart_plug_mini_2",
        "group": "Schalter",
    },
    {
        "label": "Ansage Büro",
        "service": "notify.alexa_media_buro",
        "extra": {
            "message": "Hallo, dies ist eine Ansage."
        },
        "group": "Ansagen",
    },
    {
        "label": "EG Saugen und Wischen",
        "service": "button.press",
        "entity_id":"button.roborock_s7_pro_ultra_eg_saugen_wischen",
        "group": "Rocky",
    },
    {
        "label": "EG Saugen",
        "service": "button.press",
        "entity_id":"button.roborock_s7_pro_ultra_eg_saugen",
        "group": "Rocky",
    },
    {
        "label": "DG Saugen und Wischen",
        "service": "button.press",
        "entity_id":"button.roborock_s7_pro_ultra_dg_saugen_wischen",
        "group": "Rocky",
    },


    
    # Lichter
    # {
    #     "label": "Wohnzimmer Licht AN",
    #     "service": "light.turn_on",
    #     "entity_id": "light.wohnzimmer",
    #     "group": "Lichter",
    # },
    # {
    #     "label": "Wohnzimmer Licht AUS",
    #     "service": "light.turn_off",
    #     "entity_id": "light.wohnzimmer",
    #     "group": "Lichter",
    # },
    # Schalter
    # {
    #     "label": "Steckdose Schreibtisch AN",
    #     "service": "switch.turn_on",
    #     "entity_id": "switch.schreibtisch",
    #     "group": "Schalter",
    # },
    # {
    #     "label": "Steckdose Schreibtisch AUS",
    #     "service": "switch.turn_off",
    #     "entity_id": "switch.schreibtisch",
    #     "group": "Schalter",
    # },
    # Szenen
    # {
    #     "label": "Szene: Abend",
    #     "service": "scene.turn_on",
    #     "entity_id": "scene.abend",
    #     "group": "Szenen",
    # },
    # Skripte
    # {
    #     "label": "Skript: Guten Morgen",
    #     "service": "script.turn_on",
    #     "entity_id": "script.guten_morgen",
    #     "group": "Skripte",
    # },
]

# ─── Routen ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Buttons nach Gruppe sortieren
    groups: dict[str, list] = {}
    for btn in BUTTONS:
        groups.setdefault(btn["group"], []).append(btn)
    return templates.TemplateResponse(request, "index.html", {"groups": groups})


@app.post("/trigger/{button_index}")
async def trigger(button_index: int):
    if button_index < 0 or button_index >= len(BUTTONS):
        raise HTTPException(status_code=404, detail="Button nicht gefunden")

    btn = BUTTONS[button_index]
    domain, service = btn["service"].split(".", 1)

    payload = {}
    if btn.get("entity_id"):
        payload["entity_id"] = btn["entity_id"]
    if btn.get("extra"):
        payload.update(btn["extra"])
    print (payload)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{HA_URL}/api/services/{domain}/{service}",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=response.status_code,
            detail=f"HA Fehler: {response.text}",
        )

    return {"status": "ok", "button": btn["label"]}