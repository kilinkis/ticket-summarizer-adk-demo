import logging
from pathlib import Path

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.plugins.base_plugin import BasePlugin
from google.genai import types

from .redaction import redact

MODEL = "gemini-3.8-flash"
INSTRUCTION = (Path(__file__).parent / "prompt.txt").read_text().strip()

logger = logging.getLogger(__name__)


class RedactionPlugin(BasePlugin):
    """Redacts PII from the user message before it is saved to the session or sent to the model.

    Logs only a character count, never ticket text.
    """

    def __init__(self) -> None:
        super().__init__(name="redaction")

    async def on_user_message_callback(self, *, invocation_context, user_message):
        parts = []
        for part in user_message.parts or []:
            parts.append(types.Part(text=redact(part.text)) if part.text else part)
        logger.info("ticket redacted (%d chars in)", sum(len(p.text or "") for p in user_message.parts or []))
        return types.Content(role=user_message.role, parts=parts)


root_agent = Agent(
    # Keep in sync with create_params.root_agent_name in agents-cli-manifest.yaml.
    name="ticket_summarizer",
    model=Gemini(
        model=MODEL,
        # Free tier: 5 requests/min and 20/day per model. Every retry spends quota, so keep it low.
        retry_options=types.HttpRetryOptions(attempts=2),
    ),
    instruction=INSTRUCTION,
)

app = App(
    root_agent=root_agent,
    name="app",
    plugins=[RedactionPlugin()],
)
