from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import jwt
import time
import requests

load_dotenv()

app = FastAPI(title="Falcon LiveKit Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_ISSUER = os.getenv("LIVEKIT_ISSUER", "falcon-backend")


class TokenRequest(BaseModel):
    identity: str
    room: str | None = None


@app.post("/api/token")
def create_token(req: TokenRequest):
    """Create a simple JWT grant for LiveKit client-side use.

    This uses HS256 and the LIVEKIT_API_SECRET. Replace or adapt to
    your LiveKit project requirements if you use a different signing key.
    """
    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        raise HTTPException(status_code=500, detail="LIVEKIT_API_KEY/SECRET not configured")

    now = int(time.time())
    exp = now + 60 * 60  # 1 hour

    payload = {
        "iss": LIVEKIT_ISSUER,
        "sub": LIVEKIT_API_KEY,
        "nbf": now,
        "exp": exp,
        "jti": f"{req.identity}-{now}",
        "grants": {
            "identity": req.identity,
        },
    }

    if req.room:
        payload["grants"]["room"] = req.room

    token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")
    return {"token": token}


class TTSRequest(BaseModel):
    text: str


@app.post("/api/tts")
def tts(req: TTSRequest):
    """Placeholder Murf Falcon TTS proxy.

    If `MURF_API_KEY` is set, this will attempt to POST to Murf's API.
    Otherwise, it returns a dummy JSON response. Replace with your
    account's API shape.
    """
    murf_key = os.getenv("MURF_API_KEY")
    if not murf_key:
        return {"status": "ok", "message": "skipped, no MURF_API_KEY", "text": req.text}

    # Example: placeholder endpoint — adapt to Murf's actual API
    api_url = "https://api.murf.ai/v1/tts"
    headers = {"Authorization": f"Bearer {murf_key}", "Content-Type": "application/json"}
    payload = {"text": req.text, "voice": "falcon"}

    resp = requests.post(api_url, json=payload, headers=headers)
    if resp.status_code >= 400:
        raise HTTPException(status_code=502, detail="Murf TTS error")

    # Proxy Murf response
    return resp.json()
