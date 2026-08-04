"""
insights.py

Calls OpenRouter's chat completions API once per transcribed segment,
e.g. to generate a summary, talking point, or answer based on what was
just said. Knows nothing about audio/capture/transcription -- its only
job is "given some text, give me back a model response."

Setup
-----
Set your OpenRouter key as an environment variable (never hardcode it):

    Windows (PowerShell):
        setx OPENROUTER_API_KEY "your-key-here"
        (then restart your terminal so it picks up the new variable)

    Windows (current session only):
        $env:OPENROUTER_API_KEY = "your-key-here"

Usage
-----
    from audio_transcriber.insights import OpenRouterInsights

    insights = OpenRouterInsights(model="openai/gpt-4o-mini")
    reply = insights.get_insight("We need to finalize the Q3 budget by Friday.")

Note on free models
--------------------
OpenRouter's free-tier models (id ending in ":free") occasionally return a
transient 404/429 when the underlying provider is at capacity -- this does
NOT mean the model id is wrong. Pass a `fallback_models` list to
automatically retry with another free model if the primary one is briefly
unavailable.
"""

import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(1)


DEFAULT_SYSTEM_PROMPT = (
    "You are a live meeting assistant. You will be given short snippets of "
    "transcribed speech from an ongoing conversation. Respond with a brief, "
    "useful insight, summary point, or follow-up question -- 1-2 sentences max."
)

# A few free models to fall back through if the primary one is briefly
# unavailable (common on OpenRouter's free tier during high demand).

DEFAULT_FALLBACK_MODELS = [

    "google/gemma-4-26b-a4b-it:free",
    "openai/gpt-oss-20b:free",
]


class OpenRouterInsights:
    """Thin client for OpenRouter's chat completions endpoint."""

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "openai/gpt-4o-mini",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        context_file: str = "context.md",
        timeout: int = 20,
        fallback_models: list | None = None,
    ):
        # Reads from the OPENROUTER_API_KEY environment variable by default.
        # Passing api_key explicitly is supported too, but avoid hardcoding
        # real keys directly in source files.
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No OpenRouter API key found. Set the OPENROUTER_API_KEY "
                "environment variable, or pass api_key= explicitly."
            )

        self.model = model
        self.system_prompt = system_prompt
        context_path = Path(__file__).parent / context_file

        try:
            self.meeting_context = context_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            self.meeting_context = ""
            print(f"Context file not found: {context_path}")

        self.timeout = timeout
        # Models to try (in order) if the primary model fails with a
        # transient error (404/429/5xx). Only used for models ending in
        # ":free", since paid models don't need this workaround.
        self.fallback_models = fallback_models if fallback_models is not None else DEFAULT_FALLBACK_MODELS




    def _call_model(self, model: str, text: str) -> requests.Response:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        if self.meeting_context:
            messages.append({
                "role": "system",
                "content": (
                    "The following is background information about the current meeting. "
                    "Use it to provide better insights, summaries, and answers. "
                    "Do not mention it unless it is relevant.\n\n"
                    f"{self.meeting_context}"
                ),
            })


        messages.append({
            "role": "user",
            "content": text




            ,
        })

        return requests.post(
            self.API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": messages,
            },
            timeout=self.timeout,
        )



    def get_insight(self, text: str) -> str:
        """Sends one transcribed segment to OpenRouter and returns the
        model's reply as plain text. If the primary model is a free model
        and returns a transient error (404/429/5xx), automatically retries
        with each model in fallback_models before giving up. Raises
        requests.HTTPError if every attempt fails."""
        candidates = [self.model]
        if self.model.endswith(":free"):
            candidates += [m for m in self.fallback_models if m != self.model]

        last_error = None
        for model in candidates:
            response = self._call_model(model, text)
            if response.status_code in (404, 429, 500, 502, 503):
                last_error = response
                continue
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        # Every candidate failed -- raise the last error for visibility.
        last_error.raise_for_status()