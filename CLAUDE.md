# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Run with auto-reload (development)
uvicorn main:app --reload
```

Requires a `.env` file with `HA_URL` and `HA_TOKEN` (see `.env.example`).

## Architecture

This is a single-file FastAPI app (`main.py`) with one HTML template (`templates/index.html`).

**Request flow:**
1. `GET /` — renders `index.html` with `groups` (a dict of group name → list of button dicts, derived from `BUTTONS`)
2. `POST /trigger/{button_index}` — looks up `BUTTONS[button_index]`, calls the HA REST API at `{HA_URL}/api/services/{domain}/{service}`, and returns `{"status": "ok", "button": label}`

**Button definition** (in `BUTTONS` list in `main.py`):
- `label`, `service` (`domain.service`), `group` — always required
- `entity_id` — included in the HA payload when present
- `extra` — dict merged into the HA payload (used e.g. for notify messages)

**Frontend** (`templates/index.html`): self-contained Jinja2 template with inline CSS and JS. The JS re-indexes all buttons by DOM order on load (overriding the Jinja2 loop index), then POSTs to `/trigger/{index}` on click and shows a toast with the result.
