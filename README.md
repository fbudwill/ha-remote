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

## Remote Server Update
cd /opt/ha-remote
git pull
systemctl restart ha-remote


## Remote Server Installation
Schritt-für-Schritt:
1. LXC Container in Proxmox erstellen
Im Proxmox WebUI: Create CT → z.B. Ubuntu 22.04 Template wählen
Empfohlene Ressourcen:

RAM: 256 MB
Disk: 4 GB
CPU: 1 Core

Wichtig: Eine statische IP vergeben, z.B. 192.168.1.50/24

2. Im LXC Container einrichten
apt update && apt install -y python3 python3-pip python3-venv git

# Projektordner anlegen
mkdir /opt/ha-remote && cd /opt/ha-remote

# Dateien rüberkopieren (oder direkt erstellen)
# Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Als Systemd-Service einrichten (damit es automatisch startet)
nano /etc/systemd/system/ha-remote.service
[Unit]
Description=HA Remote Panel
After=network.target

[Service]
WorkingDirectory=/opt/ha-remote
ExecStart=/opt/ha-remote/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
Restart=always
User=root

[Install]
WantedBy=multi-user.target
bashsystemctl daemon-reload
systemctl enable ha-remote
systemctl start ha-remote
```

---

**4. Erreichbar im lokalen Netz**

Danach ist die Seite für alle Geräte im Netz erreichbar unter:
```
http://192.168.1.50:8080