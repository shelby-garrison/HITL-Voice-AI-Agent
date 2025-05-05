import asyncio
import json
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
    UserInputTranscribedEvent,
)
from livekit.agents.llm import ChatMessage
from livekit.plugins import groq, silero
from human_fallback import HumanFallbackSystem


load_dotenv(dotenv_path=".env.local")
human_fallback = HumanFallbackSystem()


@function_tool
async def lookup_salon(context: RunContext, location: str):
    """Provides salon details such as timings and prices."""
    return {
        "Opening Timings": "All days except Monday, 8am to 8pm",
        "Price for Men's Haircut": "$50",
        "Price for Women's Haircut": "$60",
        "Price for Kids Haircut": "$20"
    }

# Human-in-the-loop Tool
@function_tool
async def request_human_assistance(context: RunContext, question: str):
    print("👤 Creating human request for:", question)
    request_id = human_fallback.create_request(question)
    print("🆔 Human request ID:", request_id)
    result = await asyncio.to_thread(human_fallback.wait_for_response, request_id)

    print("✅ Final result from human:", result)
    return result


# Main entrypoint
async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(
        instructions="""
        You are a friendly salon voice assistant built by LiveKit.
        Use lookup_salon to answer salon-related questions.
        If you can't answer a question, use request_human_assistance to escalate.
        Be polite, don't guess.
        """,
        tools=[lookup_salon, request_human_assistance],
    )

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=groq.STT(model="whisper-large-v3"),
        llm=groq.LLM(model="llama-3.3-70b-versatile"),
        tts=groq.TTS(model="playai-tts"),
    )

    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="Greet the user and ask how you can help today.")

    history = []

    # Handler for transcribed input
    @session.on(UserInputTranscribedEvent)
    def on_user_input(event: UserInputTranscribedEvent):
        if event.is_final:
            asyncio.create_task(handle_input(event.transcript))

    # Processing user message
    async def handle_input(user_msg):
        history.append(ChatMessage(role="user", text=user_msg))
        response = await agent.chat(history)
       

        if response.tool_calls:
           for call in response.tool_calls:
            if call.name == "request_human_assistance":
             await session.send_message("Let me check with a human. Please wait...")

            
            if not call.result:
                result = await request_human_assistance(agent, question=call.args.get("question", ""))
            else:
                result = call.result

            if result and "answer" in result:
            
                await session.send_message(result["answer"])
                history.append(ChatMessage(role="assistant", text=result["answer"]))
            else:
                await session.send_message("Still waiting on a human response. Please check back soon.")
        else:
            result_str = json.dumps(call.result) if call.result else "No result from tool."
            await session.send_message(result_str)
            history.append(ChatMessage(role="assistant", text=result_str))


    # Keeping session alive
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        print("Job cancelled, exiting cleanly.")

# cli runner
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))  