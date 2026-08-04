"""
transcribe.py

Command-line entry point + backwards-compatible alias for the
audio_transcriber package. All the actual logic now lives in:

    audio_transcriber/capture.py      - WASAPI loopback audio capture
    audio_transcriber/segmenter.py    - VAD-based pause segmentation
    audio_transcriber/transcriber.py  - faster-whisper wrapper
    audio_transcriber/pipeline.py     - wires the above together

`SystemAudioTranscriber` here is just TranscriptionPipeline under a
different name, so existing code (gui.py, ia.py) that does
`from transcribe import SystemAudioTranscriber` keeps working unchanged.

Run
---
    python transcribe.py

Press Ctrl+C to stop.
"""

import argparse

from audio_transcriber import TranscriptionPipeline

# Backwards-compatible alias -- gui.py / ia.py import this name.
SystemAudioTranscriber = TranscriptionPipeline


def main():
    parser = argparse.ArgumentParser(description="Live-transcribe your computer's audio output, segmented by pauses.")
    parser.add_argument("--model", default="base",
                         help="Whisper model size: tiny, base, small, medium, large-v3 (default: base)")
    parser.add_argument("--device", type=int, default=None,
                         help="Loopback device index to use (see --list-devices)")
    parser.add_argument("--list-devices", action="store_true",
                         help="List available loopback devices and exit")
    parser.add_argument("--save", type=str, default=None,
                         help="Path to a .txt file to append the transcript to")
    parser.add_argument("--compute-type", default="int8",
                         help="faster-whisper compute type: int8 (fast, CPU-friendly), float16, float32")
    parser.add_argument("--vad-aggressiveness", type=int, default=2, choices=[0, 1, 2, 3],
                         help="0=most permissive (catches more speech, more false positives) to 3=most aggressive")
    parser.add_argument("--silence-ms", type=int, default=600,
                         help="How much silence ends a segment / counts as 'a pause' (default 600ms)")
    parser.add_argument("--insights", action="store_true",
                         help="Send each transcribed segment to OpenRouter and print the response. "
                              "Requires the OPENROUTER_API_KEY environment variable to be set.")
    parser.add_argument("--insights-model", default="openai/gpt-4o-mini",
                         help="OpenRouter model to use for insights (default: openai/gpt-4o-mini)")
    args = parser.parse_args()

    insights = None
    if args.insights:
        from audio_transcriber import OpenRouterInsights
        insights = OpenRouterInsights(model=args.insights_model)

    pipeline = TranscriptionPipeline(
        model_size=args.model,
        compute_type=args.compute_type,
        device_index=args.device,
        vad_aggressiveness=args.vad_aggressiveness,
        silence_ms=args.silence_ms,
        save_path=args.save,
        insights=insights,
    )

    if args.list_devices:
        pipeline.list_devices()
        pipeline.audio_source.close()
        return

    pipeline.start()


if __name__ == "__main__":
    main()
