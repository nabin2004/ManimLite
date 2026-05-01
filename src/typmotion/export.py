"""Video export via PyAV — streams Skia RGBA frames into H.264 MP4."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import numpy.typing as npt

from typmotion.core import Scene
from typmotion.render import SkiaRenderer


@dataclass(slots=True)
class PyAVEncoder:
    """Encodes a rendered scene to H.264 MP4 without intermediate frame files."""

    scene: Scene
    output_path: Path
    renderer: SkiaRenderer = field(default_factory=SkiaRenderer)

    def encode(self, *, verbose: bool = True) -> Path:
        """Render every frame and mux into an MP4 container.

        Returns the output path on success.
        """
        import av

        scene = self.scene
        if scene.fps <= 0:
            raise ValueError("scene.fps must be positive")

        n_frames = max(1, round(scene.duration * scene.fps))
        dt = 1.0 / scene.fps

        w = scene.width if scene.width % 2 == 0 else scene.width + 1
        h = scene.height if scene.height % 2 == 0 else scene.height + 1

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        container = av.open(str(self.output_path), mode="w")
        stream = container.add_stream("libx264", rate=int(scene.fps))
        stream.width = w
        stream.height = h
        stream.pix_fmt = "yuv420p"
        stream.options = {"crf": "23", "preset": "medium"}

        try:
            for i in range(n_frames):
                t = min(scene.duration, (i + 1) * dt)
                rgba = self.renderer.render_frame(scene, t)
                rgb = self._rgba_to_rgb(rgba, w, h)
                video_frame = av.VideoFrame.from_ndarray(rgb, format="rgb24")
                video_frame.pts = i
                for packet in stream.encode(video_frame):
                    container.mux(packet)
                if verbose and (i % max(1, n_frames // 10) == 0 or i == n_frames - 1):
                    print(
                        f"\r  encoding: {i + 1}/{n_frames} frames",
                        end="",
                        file=sys.stderr,
                        flush=True,
                    )

            for packet in stream.encode():
                container.mux(packet)
        finally:
            container.close()

        if verbose:
            print(file=sys.stderr)

        return self.output_path

    @staticmethod
    def _rgba_to_rgb(
        rgba: npt.NDArray[np.uint8], target_w: int, target_h: int
    ) -> npt.NDArray[np.uint8]:
        """Convert RGBA (potentially odd-sized) to RGB padded to even dimensions."""
        h, w = rgba.shape[:2]
        rgb = rgba[:, :, :3]
        if h == target_h and w == target_w:
            return np.ascontiguousarray(rgb)
        padded = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        padded[:h, :w, :] = rgb
        return padded
