"""
segmenter.py

Turns a stream of fixed-size audio frames into discrete speech segments,
splitting on pauses (silence) rather than a fixed timer. Knows nothing
about where the frames come from or what happens to the segments after --
its only job is "tell me when one utterance ends and the next begins."
"""

import collections
import sys

import numpy as np

try:
    import webrtcvad
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(1)


class VoiceActivitySegmenter:
    """Consumes a generator of raw audio frames (bytes) and yields finished
    speech segments (as float32 numpy arrays, range -1.0..1.0) as soon as
    a pause -- or a max-length safety valve -- ends them."""

    def __init__(
        self,
        sample_rate: int,
        frame_ms: int,
        vad_aggressiveness: int = 2,
        padding_ms: int = 300,
        silence_ms: int = 600,
        max_segment_ms: int = 15000,
        min_segment_ms: int = 250,
    ):
        self.sample_rate = sample_rate
        self.frame_ms = frame_ms
        self.padding_ms = padding_ms
        self.silence_ms = silence_ms
        self.max_segment_ms = max_segment_ms
        self.min_segment_ms = min_segment_ms

        self._vad = webrtcvad.Vad(vad_aggressiveness)

    def segments(self, frames):
        """Generator: yields one float32 numpy array per completed speech
        segment as the frame stream is consumed."""
        num_padding_frames = max(1, self.padding_ms // self.frame_ms)
        num_silence_frames_to_end = max(1, self.silence_ms // self.frame_ms)
        max_segment_frames = max(1, self.max_segment_ms // self.frame_ms)

        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False
        voiced_frames = []
        silence_run = 0

        for frame in frames:
            is_speech = self._vad.is_speech(frame, self.sample_rate)

            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, s in ring_buffer if s])
                if num_voiced > 0.6 * ring_buffer.maxlen:
                    # Speech onset -- open segment, keep the pre-roll
                    triggered = True
                    voiced_frames.extend(f for f, s in ring_buffer)
                    ring_buffer.clear()
                    silence_run = 0
            else:
                voiced_frames.append(frame)
                silence_run = 0 if is_speech else silence_run + 1

                if silence_run >= num_silence_frames_to_end or len(voiced_frames) >= max_segment_frames:
                    segment = self._finalize(voiced_frames)
                    if segment is not None:
                        yield segment
                    triggered = False
                    voiced_frames = []
                    ring_buffer.clear()
                    silence_run = 0

    def _finalize(self, voiced_frames: list):
        """Converts a list of raw audio frames into a float32 array, or
        returns None if the segment is too short to be worth transcribing."""
        segment_ms = len(voiced_frames) * self.frame_ms
        if segment_ms < self.min_segment_ms:
            return None
        segment_bytes = b"".join(voiced_frames)
        pcm = np.frombuffer(segment_bytes, dtype=np.int16)
        return pcm.astype(np.float32) / 32768.0
