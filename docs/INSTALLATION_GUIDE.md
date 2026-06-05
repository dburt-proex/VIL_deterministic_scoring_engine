# Installation Guide

## Local Python

```bash
git clone https://github.com/dburt-proex/VIL_deterministic_scoring_engine.git
cd VIL_deterministic_scoring_engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```

## Smoke Test

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/score -H "Content-Type: application/json" -d @examples/lead_intake_signal.json
```

## Docker

```bash
docker build -t vil-engine .
docker run -p 8000:8000 vil-engine
```
