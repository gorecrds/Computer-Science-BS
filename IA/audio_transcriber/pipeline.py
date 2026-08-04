"""
pipeline.py

Wires the three independent pieces (audio capture, VAD segmentation, and
transcription) together into a runnable live-transcription pipeline, using
a background thread pair connected by a queue so capture is never blocked
waiting on the (slower) transcription step.

This is the piece to extend for new features -- e.g. run a second pipeline
against a MicrophoneAudioSource for your own voice, or add a step after
transcription that feeds text into an LLM for "insights."
"""

import queue
import threading
import time
from datetime import datetime
from pathlib import Path

from .capture import LoopbackAudioSource
from .segmenter import VoiceActivitySegmenter
from .transcriber import WhisperTranscriber


class TranscriptionPipeline:
    """Captures your computer's audio output and transcribes it live,
    segmenting speech by pauses rather than a fixed timer.

    Usage:
        p = TranscriptionPipeline(model_size="base", silence_ms=600)
        p.start()          # runs until Ctrl+C
    """

    def __init__(
        self,
        model_size: str = "tiny.en",
        compute_type: str = "int8",
        device_index: int | None = None,
        vad_aggressiveness: int = 2,
        padding_ms: int = 100,
        silence_ms: int = 350,
        max_segment_ms: int = 15000,
        min_segment_ms: int = 150,
        save_path: str | None = None,
        on_transcript=None,
        insights=None,
        on_insight=None,
    ):
        self.audio_source = LoopbackAudioSource(device_index=device_index)
        self.segmenter = VoiceActivitySegmenter(
            sample_rate=LoopbackAudioSource.SAMPLE_RATE,
            frame_ms=LoopbackAudioSource.FRAME_MS,
            vad_aggressiveness=vad_aggressiveness,
            padding_ms=padding_ms,
            silence_ms=silence_ms,
            max_segment_ms=max_segment_ms,
            min_segment_ms=min_segment_ms,
        )
        self.transcriber = WhisperTranscriber(model_size=model_size, compute_type=compute_type)

        self.silence_ms = silence_ms
        self.save_path = Path(save_path) if save_path else None

        # Optional callback: on_transcript(text: str, timestamp: str) -> None
        # Defaults to printing. Override to route text elsewhere (a UI, a
        # websocket, an LLM prompt for "insights", etc).
        self.on_transcript = on_transcript or self._default_on_transcript

        # Optional: an OpenRouterInsights (or compatible) instance with a
        # .get_insight(text) -> str method. If set, it's called once per
        # transcribed segment and the result is passed to on_insight.
        self.insights = insights
        self.on_insight = on_insight or self._default_on_insight

        self._audio_queue: "queue.Queue" = queue.Queue()
        self._stop_event = threading.Event()
        self._capture_thread: threading.Thread | None = None
        self._transcribe_thread: threading.Thread | None = None

    # ------------------------------------------------------------------ #
    # Device discovery (delegated to the audio source)
    # ------------------------------------------------------------------ #

    def list_devices(self):
        self.audio_source.list_devices()

    # ------------------------------------------------------------------ #
    # Threads
    # ------------------------------------------------------------------ #

    def _capture_loop(self):
        frames = self.audio_source.frames(self._stop_event)
        for segment in self.segmenter.segments(frames):
            self._audio_queue.put(segment)

    def _transcribe_loop(self):
        while not self._stop_event.is_set() or not self._audio_queue.empty():
            try:
                segment = self._audio_queue.get(timeout=1)
            except queue.Empty:
                continue

            text = self.transcriber.transcribe(segment)

            if text:
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.on_transcript(text, timestamp)
                if self.save_path:
                    with open(self.save_path, "a", encoding="utf-8") as f:
                        f.write(f"[{timestamp}] {text}\n")

                if self.insights is not None:
                    self._get_insight(text, timestamp)

    def _get_insight(self, text: str, timestamp: str):
        """Calls the insights client for one transcribed segment. Runs
        inline on the transcribe thread -- if a call is slow, it delays
        picking up the next queued segment. For most usage (a few seconds
        per meeting utterance) this is fine; if it becomes a bottleneck,
        this is the spot to hand off to its own thread/queue instead."""
        try:
            insight_text = self.insights.get_insight(text)
            self.on_insight(insight_text, timestamp)
        except Exception as e:
            self.on_insight(f"[insight error: {e}]", timestamp)

    def _default_on_transcript(self, text: str, timestamp: str):
        print(f"[{timestamp}] {text}", flush=True)

    def _default_on_insight(self, text: str, timestamp: str):
        print(f"  -> insight [{timestamp}]: {text}", flush=True)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def start(self):
        """Resolve the audio device, load the whisper model, and run until
        interrupted with Ctrl+C. Blocks the calling thread."""
        self.audio_source.resolve()
        print(f"Capturing system audio from: {self.audio_source.device['name']}")

        print(f"Loading whisper model '{self.transcriber.model_size}'... (first run downloads it)")
        self.transcriber.load()
        print(f"Ready. Segmenting on pauses of {self.silence_ms}ms. Listening... (Ctrl+C to stop)\n")

        self._stop_event.clear()
        self._capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._transcribe_thread = threading.Thread(target=self._transcribe_loop, daemon=True)
        self._capture_thread.start()
        self._transcribe_thread.start()

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Signal both threads to wind down and wait for them to finish."""
        print("\nStopping...")
        self._stop_event.set()
        if self._capture_thread:
            self._capture_thread.join(timeout=2)
        if self._transcribe_thread:
            self._transcribe_thread.join(timeout=5)
        self.audio_source.close()
        print("Done.")
