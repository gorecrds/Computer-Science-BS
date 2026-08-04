"""
transcriber.py

Wraps the actual speech-to-text engine (faster-whisper). Knows nothing
about audio capture or segmentation -- its only job is "given a chunk of
audio, give me back text." This is the piece to swap out if you ever want
a different STT engine or a cloud API instead of local Whisper.
"""

import sys

import numpy as np

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(1)


class WhisperTranscriber:
    """Loads a local faster-whisper model and transcribes audio segments."""

    def __init__(self, model_size: str = "base", compute_type: str = "int8", language: str = "en"):
        self.model_size = model_size
        self.compute_type = compute_type
        self.language = language
        self._model: WhisperModel | None = None

    def load(self):
        """Loads (and if needed, downloads) the whisper model. Call once
        before transcribe(); done lazily by transcribe() if skipped."""
        if self._model is None:
            self._model = WhisperModel(self.model_size, device="cpu", compute_type=self.compute_type)
        return self._model

    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribes a float32 mono audio array (16kHz) and returns the
        resulting text, stripped and joined into a single string."""
        model = self.load()
        segments, _ = model.transcribe(audio, language=self.language)
        return " ".join(seg.text.strip() for seg in segments).strip()
