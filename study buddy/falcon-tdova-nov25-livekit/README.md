# falcon-tdova-nov25-livekit

Project scaffold for a LiveKit-enabled voice assistant using Murf Falcon TTS.

Structure
```
falcon-tdova-nov25-livekit/
├── backend/          # LiveKit Agents backend with Murf Falcon TTS
├── frontend/         # React/Next.js frontend for voice interaction
├── start_app.sh      # Convenience script to start all services
└── README.md         # This file
```

Quick start (prereqs)
- Node.js (v18+), npm
- Python 3.10+
- (Optional) winget on Windows to install Node

1) Backend

```powershell
cd falcon-tdova-nov25-livekit/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

2) Frontend

```powershell
cd falcon-tdova-nov25-livekit/frontend
npm install
npm run dev
```

3) One-step (UNIX / WSL / Git Bash)

```bash
./start_app.sh
```

Configuration
- Copy `backend/.env.example` to `backend/.env` and fill values (LIVEKIT_API_KEY/SECRET, MURF_API_KEY, etc.)

Notes
- The backend provides a simple LiveKit token endpoint and a placeholder Murf TTS proxy. Replace Murf integration with your account details and desired audio pipeline.
- The frontend is a minimal Next.js app that requests a token and demonstrates how you might connect using LiveKit web SDK.
