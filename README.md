# HA Remote

Ein schlankes Web-Control-Panel für Home Assistant. Buttons im Browser lösen direkt HA-Services aus — ohne die volle HA-Oberfläche öffnen zu müssen.

## Features

- Buttons in frei benennbaren Gruppen
- Unterstützt beliebige HA-Services (Schalter, Lichter, Szenen, Skripte, Notify, ...)
- Optionale Extra-Parameter pro Button (z. B. Ansage-Text)
- Dark-Theme UI mit Toast-Feedback

---

## Voraussetzungen

- Python 3.11+
- Home Assistant mit aktivierter REST-API
- Long-Lived Access Token (in HA unter *Profil → Sicherheit → Langlebige Zugriffstoken*)

---

## Installation

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Konfigurationsdatei anlegen:

```bash
cp .env.example .env
```

`.env` ausfüllen:

```env
HA_URL=http://192.168.1.10:8123
HA_TOKEN=your_long_lived_access_token_here
```

---

## Server starten

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Aufruf im Browser: `http://localhost:8000`

Für automatischen Reload während der Entwicklung:

```bash
uvicorn main:app --reload
```

---

## Buttons konfigurieren

Alle Buttons werden direkt in `main.py` in der `BUTTONS`-Liste definiert. Jeder Eintrag ist ein Dictionary mit folgenden Feldern:

| Feld        | Pflicht | Beschreibung |
|-------------|---------|--------------|
| `label`     | ja      | Beschriftung des Buttons |
| `service`   | ja      | HA-Service im Format `domain.service` (z. B. `switch.toggle`) |
| `entity_id` | nein    | Ziel-Entity in HA (bei Services, die eine Entity benötigen) |
| `group`     | ja      | Gruppenname für die Darstellung (frei wählbar) |
| `extra`     | nein    | Zusätzliche Parameter, die an den Service übergeben werden |

### Beispiele

**Schalter toggeln**
```python
{
    "label": "Schreibtischlampe",
    "service": "switch.toggle",
    "entity_id": "switch.schreibtischlampe",
    "group": "Schalter",
}
```

**Licht einschalten**
```python
{
    "label": "Wohnzimmer AN",
    "service": "light.turn_on",
    "entity_id": "light.wohnzimmer",
    "group": "Lichter",
}
```

**Szene aktivieren**
```python
{
    "label": "Szene: Abend",
    "service": "scene.turn_on",
    "entity_id": "scene.abend",
    "group": "Szenen",
}
```

**Skript ausführen**
```python
{
    "label": "Guten Morgen",
    "service": "script.turn_on",
    "entity_id": "script.guten_morgen",
    "group": "Skripte",
}
```

**Alexa-Ansage (Notify mit Extra-Parameter)**
```python
{
    "label": "Ansage Küche",
    "service": "notify.alexa_media_kuche",
    "extra": {
        "message": "Das Essen ist fertig."
    },
    "group": "Ansagen",
}
```

**Roborock-Button drücken**
```python
{
    "label": "EG Saugen",
    "service": "button.press",
    "entity_id": "button.roborock_s7_pro_ultra_eg_saugen",
    "group": "Staubsauger",
}
```

Buttons werden auf der Oberfläche nach `group` zusammengefasst und in der Reihenfolge angezeigt, in der die Gruppen in `BUTTONS` zuerst auftauchen.

---

## Umgebungsvariablen

| Variable   | Beschreibung |
|------------|--------------|
| `HA_URL`   | Basis-URL der Home Assistant Instanz (ohne abschließenden `/`) |
| `HA_TOKEN` | Long-Lived Access Token |
