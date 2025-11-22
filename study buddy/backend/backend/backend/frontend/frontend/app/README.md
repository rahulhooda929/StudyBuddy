# Falcon-TDOVA LiveKit Agent

A real-time voice agent using **LiveKit Agents**, **Murf Falcon TTS**, and **OpenAI GPT-4o**.

## Components
1.  **Murf Falcon TTS**: Utilizes the `murf_plugin.py` adapter for ultra-low latency (<130ms) speech generation.
2.  **LiveKit VoicePipeline**: Manages the VAD (Voice Activity Detection), STT, LLM, and TTS loop.

## Setup
1.  Get API Keys for LiveKit, OpenAI, Deepgram, and Murf.ai.
2.  Fill in `backend/.env`.
3.  Run `./start_app.sh`.