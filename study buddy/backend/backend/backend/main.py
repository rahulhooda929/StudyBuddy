import asyncio
import logging
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, deepgram
from murf_plugin import MurfTTS

load_dotenv()
logger = logging.getLogger("voice-agent")

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Initialize the agent with Murf Falcon for TTS
    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata.get("vad"),
        stt=deepgram.STT(), # Deepgram is fast and pairs well with Falcon
        llm=openai.LLM(model="gpt-4o"), # Reasoning brain
        tts=MurfTTS(voice_id="en-US-cooper"), # The Custom Murf Falcon Integration
    )

    agent.start(ctx.room)

    await agent.say("Hello, I am connected using the ultra-fast Murf Falcon model. How can I help you?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))