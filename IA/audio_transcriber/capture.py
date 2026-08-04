"""
capture.py

Owns everything about getting raw audio frames off a device: finding the
right WASAPI loopback device and streaming fixed-size, resampled frames
from it. Knows nothing about VAD, segmentation, or transcription -- its
only job is "give me audio."
"""

import sys
import threading

import numpy as np

try:
    import pyaudiowpatch as pyaudio
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(1)


class LoopbackAudioSource:
    """Streams mono int16 audio frames at a fixed sample rate/frame size
    from your computer's audio OUTPUT (speakers/headphones), via WASAPI
    loopback. This is the thing to swap out if you ever want a different
    audio source (e.g. a MicrophoneAudioSource for your own voice)."""

    SAMPLE_RATE = 16000   # what whisper + webrtcvad expect
    FRAME_MS = 30          # webrtcvad only accepts 10, 20, or 30 ms frames

    def __init__(self, device_index: int | None = None):
        self.device_index = device_index
        self.frame_samples = int(self.SAMPLE_RATE * self.FRAME_MS / 1000)

        self._pyaudio = pyaudio.PyAudio()
        self.device = None  # populated by resolve()

    def list_devices(self):
        """Print all available loopback (system audio) devices."""
        print("\nAvailable loopback (system audio) devices:\n")
        for device in self._pyaudio.get_loopback_device_info_generator():
            print(f"  [{device['index']}] {device['name']}  "
                  f"(rate={int(device['defaultSampleRate'])})")
        print()

    def resolve(self):
        """Pick the loopback device to capture from: an explicit index if
        given, otherwise the loopback twin of the current default speaker.
        Stores the result on self.device and also returns it."""
        if self.device_index is not None:
            self.device = self._pyaudio.get_device_info_by_index(self.device_index)
            return self.device

        wasapi_info = self._pyaudio.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_speakers = self._pyaudio.get_device_info_by_index(
            wasapi_info["defaultOutputDevice"]
        )

        if default_speakers.get("isLoopbackDevice", False):
            self.device = default_speakers
            return self.device

        for device in self._pyaudio.get_loopback_device_info_generator():
            if default_speakers["name"] in device["name"]:
                self.device = device
                return self.device

        raise RuntimeError(
            "Could not find a loopback device for your default speakers. "
            "Try list_devices() to pick one manually."
        )

    def _resample(self, samples: np.ndarray, orig_rate: int) -> np.ndarray:
        """Simple linear-interpolation resampler (good enough for speech)."""
        if orig_rate == self.SAMPLE_RATE:
            return samples
        duration = len(samples) / orig_rate
        target_len = max(1, int(duration * self.SAMPLE_RATE))
        orig_idx = np.linspace(0, len(samples) - 1, num=len(samples))
        target_idx = np.linspace(0, len(samples) - 1, num=target_len)
        return np.interp(target_idx, orig_idx, samples).astype(np.int16)

    def frames(self, stop_event: threading.Event):
        """Yields consecutive FRAME_MS chunks of int16 mono audio at
        SAMPLE_RATE, resampled from whatever the device natively provides.
        Runs until stop_event is set. Call resolve() first."""
        if self.device is None:
            self.resolve()

        channels = self.device["maxInputChannels"]
        rate = int(self.device["defaultSampleRate"])
        native_frame_samples = int(rate * self.FRAME_MS / 1000)

        stream = self._pyaudio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=self.device["index"],
            frames_per_buffer=native_frame_samples,
        )

        try:
            while not stop_event.is_set():
                data = stream.read(native_frame_samples, exception_on_overflow=False)
                samples = np.frombuffer(data, dtype=np.int16)

                if channels > 1:
                    samples = samples.reshape(-1, channels).mean(axis=1).astype(np.int16)

                samples = self._resample(samples, rate)

                if len(samples) < self.frame_samples:
                    samples = np.pad(samples, (0, self.frame_samples - len(samples)))
                elif len(samples) > self.frame_samples:
                    samples = samples[: self.frame_samples]

                yield samples.tobytes()
        finally:
            stream.stop_stream()
            stream.close()

    def close(self):
        self._pyaudio.terminate()
