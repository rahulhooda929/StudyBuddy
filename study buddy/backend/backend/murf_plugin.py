import asyncio
import os
from typing import AsyncIterable
from livekit.agents import tts
from livekit.rtc import AudioFrame
from murf import Murf
import numpy as np

class MurfTTS(tts.TTS):
    def __init__(self, api_key: str = None, voice_id: str = "en-US-cooper"):
        super().__init__(
            capabilities=tts.TTSCapabilities(
                streaming=True,
            ),
            sample_rate=24000,
            num_channels=1,
        )
        self._api_key = api_key or os.getenv("MURF_API_KEY")
        if not self._api_key:
            raise ValueError("MURF_API_KEY is required")
        
        self._client = Murf(api_key=self._api_key)
        self._voice_id = voice_id
        self._model = "FALCON"  # The low-latency model

    def stream(self) -> tts.SynthesizeStream:
        return MurfStream(self)

class MurfStream(tts.SynthesizeStream):
    def __init__(self, tts_instance: MurfTTS):
        super().__init__(tts=tts_instance)
        self._tts = tts_instance
        self._closed = False

    async def _run(self):
        # Murf Falcon requires the full text for best context, 
        # but for streaming agents we often get chunks.
        # We collect text from the input_stream until we get a flush or completion.
        
        full_text = ""
        async for input_text in self._input_messages:
            full_text += input_text + " "
        
        if not full_text.strip():
            return

        try:
            # Murf Python SDK streaming call
            # Note: We request PCM format for raw audio handling
            audio_stream = self._tts._client.text_to_speech.stream(
                text=full_text,
                voice_id=self._tts._voice_id,
                model=self._tts._model,
                format="PCM",
                sample_rate=24000
            )

            # Process chunks (blocking generator, so we run in thread if needed, 
            # but here we iterate directly for simplicity in this demo structure)
            for chunk in audio_stream:
                if self._closed:
                    break
                if chunk:
                    # Convert raw bytes to AudioFrame
                    # Murf sends 16-bit PCM
                    data = np.frombuffer(chunk, dtype=np.int16)
                    frame = AudioFrame(
                        data=data.tobytes(),
                        sample_rate=24000,
                        num_channels=1,
                        samples_per_channel=len(data)
                    )
                    yield tts.SynthesizedAudio(frame=frame)
                    
        except Exception as e:
            print(f"Murf TTS Error: {e}")

    async def aclose(self):
        self._closed = True
        await super().aclose()