# Backend (FastAPI)

Provides two endpoints:

- `POST /api/token` - issues a temporary JWT token for LiveKit clients. Body `{ "identity": "some-id", "room": "optional-room" }`.
- `POST /api/tts` - proxy to Murf Falcon TTS (placeholder). Body `{ "text": "hello" }`.

Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or on Windows: .\.venv\Scripts\Activate.ps1 (PowerShell)
pip install -r requirements.txt
cp .env.example .env
# edit .env and fill LIVEKIT_API_KEY and LIVEKIT_API_SECRET
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Notes
- The token generation is a simplified HS256 JWT encoded with `LIVEKIT_API_SECRET`. Adjust grants/claims for your LiveKit deployment as needed.
