# ManimLite — Cinematic Black Hole Rendering Architecture

## Overview
The existing recipe (`interstellar_black_hole.py`) is a manually-assembled flat list of
`Ellipse` / `Arc` / `Line` primitives with a `Rotate` + `CameraZoom` animation pair.
It works, but it does not *scale*. The design below introduces ten interlocking systems
that collectively move ManimLite from "shape placer" toward "visual communication
engine." Each step builds on the previous and preserves backward compatibility with the
existing `Scene / Node / SkiaRenderer / PyAVEncoder` API.

---

## Step 1 — Material System

### Motivation

Color alone conflates surface appearance with light interaction. A `Material` separates
those concerns, letting a single palette entry drive emissive glow, heat shimmer,
transparency, and tint independently.

### Class Definition

```python
# manimlite/materials.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Material:
    """Surface appearance descriptor.

    Parameters
    ----------
    emissive : float
        Self-luminance [0–1].  0 = purely reflective/absorptive;
        1 = blazing hot, contributes fully to bloom extraction.
    heat : float
        Thermal intensity [0–1].  Shifts hue toward orange-white on the
        Planckian locus. Used by the atmospheric renderer (Step 9) to tint
        bloom halos.
    opacity : float
        Alpha multiplier applied after the node's fill_color alpha.  Allows
        the material to globally dim a layer without re-specifying every color.
    glow_color : str
        Hex RGBA ("#RRGGBBAA") or RGB ("#RRGGBB") used when bloom is extracted
        from this material's pixels.  Defaults to a warm white if empty.
    roughness : float
        Perceptual roughness [0–1].  0 = mirror-like (sharp edges);
        1 = fully diffuse (soft, no specular).  Currently used by the
        grain pass (Step 9) — rough surfaces get more grain.
    metallic : float
        Controls whether specular highlights use the glow_color (metallic=1)
        or white (metallic=0).  Future use for multi-pass Skia paint stacks.
    displacement : float
        Maximum displacement radius (px) for procedural distortion (Step 4).
        0 = undisturbed geometry.
    """

    emissive: float = 0.0
    heat: float = 0.0
    opacity: float = 1.0
    glow_color: str = "#FFF5D6FF"
    roughness: float = 0.5
    metallic: float = 0.0
    displacement: float = 0.0


# ── Canonical material library ─────────────────────────────────────────────

# Plasma so hot it borders white; outer coronal edge of an accretion disk.
HOT_PLASMA = Material(
    emissive=0.95,
    heat=1.0,
    opacity=0.85,
    glow_color="#FFEECC",
    roughness=0.1,
    metallic=0.0,
    displacement=4.0,
)

# The transitional band between inner hot core and cooler outer corona.
WARM_DISK = Material(
    emissive=0.65,
    heat=0.7,
    opacity=0.72,
    glow_color="#FFAA4488",
    roughness=0.25,
    metallic=0.0,
    displacement=6.0,
)

# Outer diffuse corona; cooler, more transparent, larger displacement.
COOL_CORONA = Material(
    emissive=0.30,
    heat=0.35,
    opacity=0.55,
    glow_color="#CC441188",
    roughness=0.6,
    metallic=0.0,
    displacement=9.0,
)

# The photon ring: tight, bright, almost no displacement.
PHOTON_RING = Material(
    emissive=0.90,
    heat=0.5,
    opacity=0.80,
    glow_color="#F9E7B0",
    roughness=0.05,
    metallic=0.3,
    displacement=1.5,
)

# Event horizon: perfect absorber, zero emissive, zero displacement.
EVENT_HORIZON = Material(
    emissive=0.0,
    heat=0.0,
    opacity=1.0,
    glow_color="#000000",
    roughness=1.0,
    metallic=0.0,
    displacement=0.0,
)

# Wrapped-light arcs: faint lensed hints at the disk edge.
LENSED_ARC = Material(
    emissive=0.45,
    heat=0.4,
    opacity=0.40,
    glow_color="#FFD7A044",
    roughness=0.4,
    metallic=0.0,
    displacement=2.0,
)

# Star field: tiny bright points, low heat, negligible displacement.
STAR_FIELD = Material(
    emissive=0.70,
    heat=0.15,
    opacity=1.0,
    glow_color="#FFFFFF",
    roughness=0.0,
    metallic=0.0,
    displacement=0.0,
)

# Glint line: the subtle cross through the center (diffraction spike).
DIFFRACTION_SPIKE = Material(
    emissive=0.25,
    heat=0.0,
    opacity=0.12,
    glow_color="#FFFFFF18",
    roughness=0.9,
    metallic=0.0,
    displacement=0.0,
)
```

### Integration with existing shapes

Shapes do not currently accept a `material` kwarg. The minimal change is to
store the material as an attribute and have `SkiaRenderer` read it:

```python
class Ellipse(Node):
    def __init__(self, ..., material: Material | None = None):
        super().__init__(...)
        self.material = material or Material()
```

`SkiaRenderer.draw_node()` then multiplies `material.opacity` into the computed
paint alpha before calling `canvas.drawOval(...)`.

---

## Step 2 — Shape Grammar (Semantic Nodes)

### Motivation

Manually adding seven `Ellipse` calls to assemble a disk is fragile and
unreadable. A `build()` protocol lets each semantic object declare its own
geometry, materials, and child hierarchy once.

### Base protocol

```python
# manimlite/core.py  (extend existing Node)

class BuildableNode(Node):
    """Node that constructs its subtree lazily on first render."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._built = False

    def build(self) -> None:  # override in subclasses
        raise NotImplementedError

    def _ensure_built(self) -> None:
        if not self._built:
            self.build()
            self._built = True
```

### DiskBand

```python
# manimlite/shapes/disk_band.py

from manimlite.core import BuildableNode
from manimlite.materials import Material, WARM_DISK
from manimlite.shapes import Ellipse


class DiskBand(BuildableNode):
    """Single toroidal band of an accretion disk.

    Parameters
    ----------
    radius : float   Half-width (rx) of the disk ellipse in pixels.
    thickness : float  Vertical half-height (ry) in pixels.
    material : Material  Surface material driving color, emissive, opacity.
    fill_color : str   RGBA hex; material.opacity is multiplied on top.
    stroke_color : str  RGBA hex for outline; pass None to suppress.
    stroke_width : float  Outline width in pixels.
    """

    def __init__(
        self,
        radius: float,
        thickness: float,
        fill_color: str,
        material: Material = WARM_DISK,
        stroke_color: str | None = None,
        stroke_width: float = 0.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.radius = radius
        self.thickness = thickness
        self.fill_color = fill_color
        self.material = material
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    def build(self) -> None:
        self.add(
            Ellipse(
                x=0.0,
                y=0.0,
                rx=self.radius,
                ry=self.thickness,
                fill_color=self.fill_color,
                stroke_color=self.stroke_color,
                stroke_width=self.stroke_width,
                material=self.material,
            )
        )
```

### AccretionDisk

```python
# manimlite/shapes/accretion_disk.py

from manimlite.core import BuildableNode
from manimlite.materials import HOT_PLASMA, WARM_DISK, COOL_CORONA
from .disk_band import DiskBand


class AccretionDisk(BuildableNode):
    """Three-layer accretion disk: outer corona → main slab → inner hot strip.

    Parameters
    ----------
    radius : float   Outer disk radius (px).
    """

    def __init__(self, radius: float = 300.0, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

    def build(self) -> None:
        r = self.radius
        # Outer diffuse corona
        self.add(DiskBand(radius=r + 48,  thickness=56, fill_color="#CC4D0088",
                          material=COOL_CORONA))
        # Lensed offset band (artistic duplication)
        self.add(DiskBand(radius=r,       thickness=36, fill_color="#FFB84D55",
                          material=WARM_DISK, stroke_color="#FFCC8833",
                          stroke_width=1.5, x=0.0, y=-36.0))
        # Main glowing slab
        self.add(DiskBand(radius=r + 2,   thickness=42, fill_color="#E85D0477",
                          material=WARM_DISK, stroke_color="#FFAA0044",
                          stroke_width=2.0))
        # Inner hot strip
        self.add(DiskBand(radius=r - 16,  thickness=11, fill_color="#FFFFFF55",
                          material=HOT_PLASMA))
```

### PhotonRing

```python
# manimlite/shapes/photon_ring.py

import math
from manimlite.core import BuildableNode
from manimlite.materials import PHOTON_RING as PM
from manimlite.shapes import Arc, Ellipse


class PhotonRing(BuildableNode):
    """Bright stroke ring + two lensed arc hints."""

    def __init__(self, radius: float = 70.0, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

    def build(self) -> None:
        r = self.radius
        # Sharp photon ring stroke
        self.add(Ellipse(x=0, y=0, rx=r, ry=r,
                         fill_color="#00000000",
                         stroke_color="#F9E7B0CC", stroke_width=2.6,
                         material=PM))
        # Outer diffuse halo ring
        self.add(Ellipse(x=0, y=0, rx=r + 14, ry=r + 14,
                         fill_color="#00000000",
                         stroke_color="#FFF5D633", stroke_width=1.2,
                         material=PM))
        # Lensed arc pair
        for start, end in [(0.05, 0.42), (1.08, 1.45)]:
            self.add(Arc(x=0, y=0, radius=r + 204,
                         start_angle=math.pi * start, end_angle=math.pi * end,
                         stroke_color="#FFD7A033", stroke_width=3.0,
                         material=PM))
```

### EventHorizon

```python
# manimlite/shapes/event_horizon.py

from manimlite.core import BuildableNode
from manimlite.materials import EVENT_HORIZON as EH, DIFFRACTION_SPIKE as DS
from manimlite.shapes import Ellipse, Line


class EventHorizon(BuildableNode):
    """Dark shadow disk + optional diffraction spike."""

    def __init__(self, radius: float = 76.0, spike: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.spike = spike

    def build(self) -> None:
        r = self.radius
        self.add(Ellipse(x=0, y=0, rx=r, ry=r,
                         fill_color="#030203",
                         stroke_color=None, stroke_width=0.0,
                         material=EH))
        if self.spike:
            self.add(Line(x0=-r * 1.45, y0=0, x1=r * 1.45, y1=0,
                          stroke_color="#FFFFFF18", stroke_width=1.0,
                          material=DS))


```

### Top-level BlackHole semantic object

```python
# manimlite/shapes/black_hole.py

from manimlite.core import BuildableNode
from .accretion_disk import AccretionDisk
from .photon_ring import PhotonRing
from .event_horizon import EventHorizon


class BlackHole(BuildableNode):
    """Complete Gargantua-style black hole scene object.

    Usage::

        bh = BlackHole(radius=76, disk_radius=300, style="interstellar")
        scene.add_node(bh)

    Parameters
    ----------
    radius : float          Shadow disk radius (px).
    disk_radius : float     Outer accretion disk radius (px).
    style : str             Reserved for future style tokens (Step 4).
    """

    def __init__(
        self,
        radius: float = 76.0,
        disk_radius: float = 300.0,
        style: str = "interstellar",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.radius = radius
        self.disk_radius = disk_radius
        self.style = style

    def build(self) -> None:
        self.add(AccretionDisk(radius=self.disk_radius))
        self.add(PhotonRing(radius=self.radius - 6))
        self.add(EventHorizon(radius=self.radius))
```

### Refactored scene entry point

```python
# Before (flat, fragile):
g.add(Ellipse(...))
g.add(Ellipse(...))
g.add(Arc(...))
# ... seven more lines

# After (semantic, composable):
bh = BlackHole(radius=76, disk_radius=300, style="interstellar", x=CX, y=CY)
scene.add_node(bh)
```

---

## Step 3 — Procedural Distortion

### Motivation

Perfect ellipses read as computer-generated immediately. Controlled noise breaks
the synthetic look without destroying the underlying geometry.

### DistortedEllipse

```python
# manimlite/shapes/distorted_ellipse.py

from __future__ import annotations
import numpy as np
import skia
from manimlite.core import Node
from manimlite.materials import Material


def _perlin_1d(theta: np.ndarray, frequency: float, seed: int = 0) -> np.ndarray:
    """Minimal 1-D smooth noise via sinusoidal superposition (no dependency)."""
    rng = np.random.default_rng(seed)
    phases = rng.uniform(0, 2 * np.pi, 8)
    amps = rng.uniform(0.5, 1.0, 8) * (0.5 ** np.arange(8))
    out = np.zeros_like(theta)
    for k, (ph, am) in enumerate(zip(phases, amps), 1):
        out += am * np.sin(k * frequency * theta + ph)
    return out / out.std()  # normalise to σ=1


class DistortedEllipse(Node):
    """Ellipse whose radius is perturbed by smooth noise.

    Parameters
    ----------
    rx, ry : float      Base semi-axes.
    noise_amp : float   Displacement amplitude (px).  Overridden by
                        material.displacement if a material is supplied.
    noise_freq : float  Spatial frequency of deformation.  Higher = more
                        wrinkles.  Typical range 1.5–6.0.
    n_pts : int         Path resolution; 256–512 is sufficient for 1280px.
    flatten : float     Vertical squash factor in (0, 1].  1.0 = circle.
                        0.15 mimics disk foreshortening.
    seed : int          RNG seed for deterministic noise.
    material : Material Surface material.
    fill_color : str    RGBA hex.
    stroke_color : str  RGBA hex or None.
    stroke_width : float
    """

    def __init__(
        self,
        rx: float,
        ry: float,
        noise_amp: float = 6.0,
        noise_freq: float = 3.0,
        n_pts: int = 512,
        flatten: float = 1.0,
        seed: int = 0,
        material: Material | None = None,
        fill_color: str = "#FFFFFF88",
        stroke_color: str | None = None,
        stroke_width: float = 0.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.rx = rx
        self.ry = ry
        self.material = material or Material()
        # material.displacement overrides explicit noise_amp when set
        amp = self.material.displacement if self.material.displacement > 0 else noise_amp
        self.noise_amp = amp
        self.noise_freq = noise_freq
        self.n_pts = n_pts
        self.flatten = flatten
        self.seed = seed
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self._path: skia.Path | None = None

    # ── Geometry ─────────────────────────────────────────────────────────

    def _build_path(self, t: float = 0.0) -> skia.Path:
        """Build a skia.Path for the distorted ellipse.

        t is a time parameter [0, 1] that slowly evolves the noise, creating
        a subtle living deformation even without an explicit Wobble animation.
        """
        theta = np.linspace(0, 2 * np.pi, self.n_pts, endpoint=False)
        noise = _perlin_1d(theta, self.noise_freq, seed=self.seed)
        # Time-varying drift: low-frequency oscillation of the displacement
        time_mod = 1.0 + 0.15 * np.sin(2 * np.pi * t + theta * 0.5)
        r = self.rx + noise * self.noise_amp * time_mod
        x_pts = r * np.cos(theta)
        y_pts = r * self.flatten * np.sin(theta)

        path = skia.Path()
        path.moveTo(float(x_pts[0]), float(y_pts[0]))
        for xi, yi in zip(x_pts[1:], y_pts[1:]):
            path.lineTo(float(xi), float(yi))
        path.close()
        return path

    # SkiaRenderer will call draw(canvas, t) on every frame.
    def draw(self, canvas: skia.Canvas, t: float = 0.0) -> None:
        path = self._build_path(t)
        paint = skia.Paint(AntiAlias=True)
        if self.fill_color and self.fill_color != "#00000000":
            paint.setStyle(skia.Paint.kFill_Style)
            paint.setColor(skia.Color4f.FromColor(int(self.fill_color.lstrip("#"), 16)))
            canvas.drawPath(path, paint)
        if self.stroke_color:
            paint.setStyle(skia.Paint.kStroke_Style)
            paint.setStrokeWidth(self.stroke_width)
            paint.setColor(skia.Color4f.FromColor(int(self.stroke_color.lstrip("#"), 16)))
            canvas.drawPath(path, paint)
```

### Usage inside AccretionDisk

Replace the outer corona `DiskBand` with a `DistortedEllipse`:

```python
# In AccretionDisk.build():
self.add(
    DistortedEllipse(
        rx=r + 48,
        ry=(r + 48) * 0.16,    # flatten ≈ disk foreshortening
        flatten=0.16,
        noise_amp=0.0,          # let material.displacement drive it
        noise_freq=3.5,
        material=COOL_CORONA,   # displacement=9.0 from material
        fill_color="#CC4D0088",
    )
)
```

---

## Step 4 — Style Tokens

### Motivation

Hard-coded hex strings scattered across a file make restyling a search-and-replace
nightmare. A style token dict gives a single source of truth.

### Token schema

```python
# manimlite/styles.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CosmicStyleTokens:
    """Color and weight tokens for a cosmic / astrophysical scene.

    All colors are RGBA hex strings ("#RRGGBBAA").
    """

    # Disk layers
    disk_outer: str = "#CC4D0088"
    disk_lensed: str = "#FFB84D55"
    disk_lensed_stroke: str = "#FFCC8833"
    disk_main: str = "#E85D0477"
    disk_main_stroke: str = "#FFAA0044"
    disk_inner: str = "#FFFFFF55"

    # Photon ring
    photon_ring: str = "#F9E7B0CC"
    photon_ring_halo: str = "#FFF5D633"
    lensed_arc: str = "#FFD7A033"

    # Shadow & background
    shadow: str = "#030203"
    space_lo: str = "#0A1628"
    space_hi: str = "#000000"

    # Stars
    star_colors: tuple = ("#FFFFFF", "#E8ECFF", "#FFEEDD", "#D0E8FF")

    # Atmospheric
    bloom_tint: str = "#FFEECC88"
    grain_intensity: float = 0.018
    haze_opacity: float = 0.04

    # Stroke weights
    photon_ring_width: float = 2.6
    photon_halo_width: float = 1.2
    lensed_arc_width: float = 3.0
    spike_width: float = 1.0


# Built-in presets
COSMIC_STYLE = CosmicStyleTokens()   # default warm palette

MONOCHROME_STYLE = CosmicStyleTokens(
    disk_outer="#66666688",
    disk_lensed="#99999955",
    disk_lensed_stroke="#AAAAAA33",
    disk_main="#77777777",
    disk_main_stroke="#AAAAAA44",
    disk_inner="#FFFFFF55",
    photon_ring="#FFFFFFCC",
    photon_ring_halo="#FFFFFF33",
    lensed_arc="#FFFFFF22",
    bloom_tint="#FFFFFF44",
)

COLD_QUASAR_STYLE = CosmicStyleTokens(
    disk_outer="#0044CC88",
    disk_lensed="#2266FF55",
    disk_lensed_stroke="#4488FF33",
    disk_main="#0033AA77",
    disk_main_stroke="#2255FF44",
    disk_inner="#AACCFFAA",
    photon_ring="#C8E8FFCC",
    photon_ring_halo="#88BBFF33",
    lensed_arc="#99CCFF22",
    bloom_tint="#AADDFF88",
    space_lo="#000A18",
)
```

### Wiring styles into BlackHole

```python
class BlackHole(BuildableNode):
    def __init__(self, ..., style: str | CosmicStyleTokens = "interstellar", **kwargs):
        ...
        if isinstance(style, str):
            self._tokens = {"interstellar": COSMIC_STYLE,
                            "mono": MONOCHROME_STYLE,
                            "quasar": COLD_QUASAR_STYLE}.get(style, COSMIC_STYLE)
        else:
            self._tokens = style

    def build(self) -> None:
        t = self._tokens
        self.add(AccretionDisk(radius=self.disk_radius, tokens=t))
        self.add(PhotonRing(radius=self.radius - 6, tokens=t))
        self.add(EventHorizon(radius=self.radius))
```

---

## Step 5 — Motion Grammar

### Motivation

`Rotate(angle0, angle1)` is a single rigid transform. Real astronomical objects
have turbulence, wobble, and differential rotation. A `CosmicRotation` encapsulates
those degrees of freedom.

### CosmicRotation

```python
# manimlite/animations/cosmic_rotation.py

from __future__ import annotations
import math
import numpy as np
from manimlite.core import Node


class CosmicRotation:
    """Cinematic rotation with optional turbulence and wobble.

    Parameters
    ----------
    speed : float
        Base angular velocity in full rotations per second.  0.2 = one
        rotation every 5 s; equivalent to old Rotate(0, 2π × N_TURNS).
    turbulence : float
        Amplitude of high-frequency angular noise (radians).  0.03 produces
        a subtle shimmer; 0.15 gives a violent churn.
    wobble : float
        Amplitude of low-frequency precession (radians).  This adds a slow
        nod to the disk plane, mimicking orbital inclination drift.
    wobble_period : float
        Period of the wobble oscillation in seconds.  Default 8 s.
    seed : int
        RNG seed for turbulence noise.
    """

    def __init__(
        self,
        speed: float = 0.2,
        turbulence: float = 0.03,
        wobble: float = 0.01,
        wobble_period: float = 8.0,
        seed: int = 42,
    ):
        self.speed = speed
        self.turbulence = turbulence
        self.wobble = wobble
        self.wobble_period = wobble_period
        self._rng = np.random.default_rng(seed)
        # Pre-bake turbulence offsets for determinism
        self._turb_phases = self._rng.uniform(0, 2 * math.pi, 6)

    def angle_at(self, t: float) -> float:
        """Return total rotation angle (radians) at time t (seconds)."""
        base = 2 * math.pi * self.speed * t

        # Turbulence: sum of sinusoids at incommensurable frequencies
        turb = sum(
            self.turbulence * math.sin(f * t + ph)
            for f, ph in zip([1.7, 3.1, 5.3, 7.9, 11.2, 13.7], self._turb_phases)
        )

        # Low-frequency wobble (precession)
        wob = self.wobble * math.sin(2 * math.pi * t / self.wobble_period)

        return base + turb + wob

    # ManimLite animation protocol
    def apply(self, node: Node, t: float, _t0: float, _t1: float) -> None:
        node.rotation = self.angle_at(t - _t0)
```

### Usage

```python
scene.add_animation(
    0.0,
    DURATION,
    disk_root,
    CosmicRotation(speed=0.2, turbulence=0.03, wobble=0.01),
)
```

---

## Step 6 — Secondary Motion System (Hierarchy of Motion)

### Motivation

A single `Rotate` applied to the disk root spins everything in lock-step. Real
cinematic sequences use *motion hierarchy*: the disk spins fast, the glow lags
behind, particles drift independently, lensing pulses on its own frequency.

### Architecture

```
disk_root  ←── CosmicRotation(speed=0.20)        # base spin
  └─ glow_node  ←── GlowLag(lag=0.15)            # glow lags 0.15 s behind
  └─ particle_node  ←── ParticleDrift(...)        # independent drift
  └─ lensing_node  ←── LensingPulse(freq=0.8)    # subtle breathing
```

### GlowLag

```python
# manimlite/animations/secondary.py

class GlowLag:
    """Applies the parent's rotation with a time delay, creating inertia."""

    def __init__(self, lag: float = 0.15, parent_rotation_fn=None):
        self.lag = lag
        self._parent_fn = parent_rotation_fn  # callable(t) → angle

    def apply(self, node, t, t0, t1):
        if self._parent_fn:
            node.rotation = self._parent_fn(max(t0, t - self.lag) - t0)


class LensingPulse:
    """Oscillates a node's opacity to simulate gravitational lensing shimmer.

    Parameters
    ----------
    freq : float   Oscillation frequency in Hz.
    amp : float    Opacity amplitude [0–1].  0.05 = barely perceptible.
    base_opacity : float  Resting opacity.
    """

    def __init__(self, freq: float = 0.8, amp: float = 0.05,
                 base_opacity: float = 0.80):
        self.freq = freq
        self.amp = amp
        self.base_opacity = base_opacity

    def apply(self, node, t, t0, t1):
        import math
        node.opacity = self.base_opacity + self.amp * math.sin(
            2 * math.pi * self.freq * (t - t0)
        )


class ParticleDrift:
    """Translates a particle layer along a Lissajous path.

    Parameters
    ----------
    ax, ay : float   Amplitude in x and y (px).
    fx, fy : float   Frequency in x and y (Hz).
    phase : float    Phase offset (radians).
    """

    def __init__(self, ax=4.0, ay=2.0, fx=0.11, fy=0.17, phase=0.0):
        self.ax, self.ay = ax, ay
        self.fx, self.fy = fx, fy
        self.phase = phase

    def apply(self, node, t, t0, t1):
        import math
        dt = t - t0
        node.x += self.ax * math.sin(2 * math.pi * self.fx * dt + self.phase)
        node.y += self.ay * math.cos(2 * math.pi * self.fy * dt)
```

### Wiring in `build_scene()`

```python
disk_root = Node(x=CX, y=CY)
bh = BlackHole(radius=76, disk_radius=300, style="interstellar")
disk_root.add(bh)

motion = CosmicRotation(speed=0.2, turbulence=0.03, wobble=0.01)
scene.add_animation(0.0, DURATION, disk_root, motion)

# Glow sub-layer lags behind the disk spin
glow_ring = bh._photon_ring_node   # exposed reference after build()
scene.add_animation(0.0, DURATION, glow_ring,
                    GlowLag(lag=0.12, parent_rotation_fn=motion.angle_at))

# Lensing arcs pulse on a sub-second frequency
lensing = bh._lensed_arcs_node
scene.add_animation(0.0, DURATION, lensing, LensingPulse(freq=0.75, amp=0.06))
```

---

## Step 7a — Composition / Motion Layer System

### MotionLayer protocol

```python
# manimlite/composition/motion_layers.py

from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass


class MotionLayer:
    """Abstract base for composable motion contributions."""

    def sample(self, t: float) -> tuple[float, float, float]:
        """Return (dx, dy, d_rotation) at time t."""
        raise NotImplementedError


@dataclass
class BaseMotion(MotionLayer):
    """Constant angular rotation."""
    angular_velocity: float = 0.2  # rotations/s

    def sample(self, t):
        return 0.0, 0.0, 2 * math.pi * self.angular_velocity * t


@dataclass
class TurbulenceMotion(MotionLayer):
    """High-frequency angular jitter."""
    amplitude: float = 0.03
    seed: int = 0

    def __post_init__(self):
        rng = np.random.default_rng(self.seed)
        self._freqs = rng.uniform(1.5, 14.0, 6)
        self._phases = rng.uniform(0, 2 * math.pi, 6)

    def sample(self, t):
        noise = sum(
            self.amplitude * math.sin(f * t + p)
            for f, p in zip(self._freqs, self._phases)
        )
        return 0.0, 0.0, noise


@dataclass
class InertiaMotion(MotionLayer):
    """Exponential lag toward a target angle — creates follow-through."""
    target_fn: object = None      # callable(t) → angle
    inertia: float = 0.85         # [0–1]; higher = more lag
    _current: float = 0.0

    def sample(self, t):
        if self.target_fn:
            target = self.target_fn(t)
            self._current += (1 - self.inertia) * (target - self._current)
        return 0.0, 0.0, self._current


@dataclass
class NoiseMotion(MotionLayer):
    """Smooth 2-D translational drift using band-limited noise."""
    amp_x: float = 3.0
    amp_y: float = 1.5
    freq: float = 0.07

    def sample(self, t):
        dx = self.amp_x * math.sin(2 * math.pi * self.freq * t)
        dy = self.amp_y * math.cos(2 * math.pi * self.freq * 1.3 * t)
        return dx, dy, 0.0


class CompositeMotion(MotionLayer):
    """Linear superposition of motion layers.

    Usage::

        motion = CompositeMotion([
            BaseMotion(angular_velocity=0.2),
            TurbulenceMotion(amplitude=0.03),
            InertiaMotion(target_fn=..., inertia=0.9),
        ])
    """

    def __init__(self, layers: list[MotionLayer]):
        self.layers = layers

    def sample(self, t):
        dx = dy = dr = 0.0
        for layer in self.layers:
            ldx, ldy, ldr = layer.sample(t)
            dx += ldx; dy += ldy; dr += ldr
        return dx, dy, dr

    def apply(self, node, t, t0, _t1):
        dx, dy, dr = self.sample(t - t0)
        node.x += dx
        node.y += dy
        node.rotation = dr
```

---

## Step 7b — Composition / Importance System

### Motivation

Scene elements should compete for visual attention in a principled way. Assigning
an `importance` scalar lets the renderer automatically modulate brightness,
contrast, and blur for each node without manual per-element tuning.

### ImportanceNode

```python
# manimlite/composition/importance.py

from manimlite.core import Node


class ImportanceNode(Node):
    """Node with a visual importance weight.

    The renderer reads `.importance` and derives:
        brightness_scale = 0.4 + 0.6 * importance
        contrast_boost   = 1.0 + 0.5 * importance
        saturation_scale = 0.6 + 0.4 * importance
        blur_radius      = max(0, (1.0 - importance) * 4.0)  # px Gaussian
    """

    def __init__(self, importance: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.importance = max(0.0, min(1.0, importance))

    @property
    def derived_brightness(self) -> float:
        return 0.4 + 0.6 * self.importance

    @property
    def derived_blur_radius(self) -> float:
        return max(0.0, (1.0 - self.importance) * 4.0)
```

### Usage

```python
black_hole_node = ImportanceNode(importance=1.0, x=CX, y=CY)
star_field_node = ImportanceNode(importance=0.2, x=0.0, y=0.0)
```

`SkiaRenderer.draw_node()` checks for `ImportanceNode` and applies an
`skia.ColorFilter` before painting the subtree.

---

## Step 8 — Camera Language

### Motivation

`CameraZoom(zoom0, zoom1)` is a linear scale with no personality. A `CameraRig`
adds inertia, cinematic drift, and a target-following mode.

### CameraRig

```python
# manimlite/animations/camera_rig.py

from __future__ import annotations
import math
import numpy as np
from manimlite.core import Node


class CameraRig:
    """Cinematic camera with inertia, drift, and target tracking.

    Parameters
    ----------
    target : Node | None
        Node whose world position the camera follows.  None = static.
    zoom_start : float   Initial zoom factor.
    zoom_end : float     Final zoom factor.
    inertia : float
        Camera lag [0–1].  0 = instant snap; 0.95 = very sluggish.
        Creates the "slow lock-on" feel of documentary cameras.
    drift_amp : float
        Low-frequency translational drift amplitude (px).  Adds handheld feel.
    drift_freq : float
        Frequency of drift oscillation (Hz).  0.03–0.08 is imperceptible but
        adds life.
    seed : int
        Drift RNG seed.
    """

    def __init__(
        self,
        target: Node | None = None,
        zoom_start: float = 1.0,
        zoom_end: float = 1.065,
        inertia: float = 0.9,
        drift_amp: float = 0.8,
        drift_freq: float = 0.05,
        seed: int = 7,
    ):
        self.target = target
        self.zoom_start = zoom_start
        self.zoom_end = zoom_end
        self.inertia = inertia
        self.drift_amp = drift_amp
        self.drift_freq = drift_freq
        rng = np.random.default_rng(seed)
        self._drift_phases = rng.uniform(0, 2 * math.pi, 3)

        self._current_zoom = zoom_start
        self._current_x = 0.0
        self._current_y = 0.0

    def _target_zoom(self, t: float, duration: float) -> float:
        alpha = t / duration if duration > 0 else 1.0
        return self.zoom_start + alpha * (self.zoom_end - self.zoom_start)

    def _drift_offset(self, t: float) -> tuple[float, float]:
        f = self.drift_freq
        a = self.drift_amp
        p = self._drift_phases
        dx = a * math.sin(2 * math.pi * f * t + p[0]) + 0.4 * a * math.sin(
            2 * math.pi * f * 2.3 * t + p[1]
        )
        dy = a * math.cos(2 * math.pi * f * 1.7 * t + p[2])
        return dx, dy

    def apply(self, scene_root, t, t0, t1):
        dt = t - t0
        duration = t1 - t0
        target_zoom = self._target_zoom(dt, duration)
        # Inertia filter
        self._current_zoom += (1.0 - self.inertia) * 0.016 * (
            target_zoom - self._current_zoom
        )
        dx, dy = self._drift_offset(dt)
        # Apply to scene root transform (ManimLite Scene exposes camera attrs)
        scene_root.camera_zoom = self._current_zoom
        scene_root.camera_tx = dx
        scene_root.camera_ty = dy
```

### Usage

```python
rig = CameraRig(
    target=disk_root,
    zoom_start=1.0,
    zoom_end=1.065,
    inertia=0.9,
    drift_amp=1.2,
    drift_freq=0.04,
)
scene.add_animation(0.0, DURATION, scene.root, rig)
```

---

## Step 9 — Atmospheric Rendering

### Doctrine

> One subtle bloom. One subtle grain. One subtle haze. That's enough.

All three are post-process passes applied *after* scene compositing.
They live in `SkiaRenderer` as an optional `AtmosphericPass`.

### BloomPass

```python
# manimlite/rendering/atmospheric.py

from __future__ import annotations
import numpy as np
import skia


class BloomPass:
    """Extracts bright regions, blurs them, and adds back.

    Algorithm::

        render scene → np.array
        threshold: keep pixels where luminance > threshold
        Gaussian blur (sigma)
        blend: out = scene + bloom * strength

    Parameters
    ----------
    threshold : float   Luminance threshold [0–1].  0.75 = only brightest.
    sigma : float       Blur radius (px) of the Gaussian kernel.
    strength : float    Blend weight of bloom layer.  0.25 = subtle.
    tint : str          RGBA hex; tints the bloom halo (e.g. "#FFEECC88").
    """

    def __init__(
        self,
        threshold: float = 0.75,
        sigma: float = 14.0,
        strength: float = 0.25,
        tint: str = "#FFEECC",
    ):
        self.threshold = threshold
        self.sigma = sigma
        self.strength = strength
        self.tint = tint

    def apply(self, pixels: np.ndarray) -> np.ndarray:
        """pixels: float32 RGBA array, shape (H, W, 4), range [0, 1]."""
        from scipy.ndimage import gaussian_filter
        lum = 0.2126 * pixels[..., 0] + 0.7152 * pixels[..., 1] + 0.0722 * pixels[..., 2]
        mask = (lum > self.threshold)[..., np.newaxis]
        bright = pixels * mask
        blurred = gaussian_filter(bright, sigma=[self.sigma, self.sigma, 0])
        return np.clip(pixels + blurred * self.strength, 0.0, 1.0)


class GrainPass:
    """Adds fine photographic grain.

    Parameters
    ----------
    intensity : float   Grain amplitude [0–1].  0.018 is barely perceptible.
    seed : int          RNG seed for deterministic grain per frame.
    """

    def __init__(self, intensity: float = 0.018, seed: int = 0):
        self.intensity = intensity
        self.seed = seed

    def apply(self, pixels: np.ndarray, frame: int = 0) -> np.ndarray:
        rng = np.random.default_rng(self.seed + frame)
        grain = rng.standard_normal(pixels.shape[:2])[..., np.newaxis] * self.intensity
        return np.clip(pixels + grain, 0.0, 1.0)


class HazePass:
    """Adds a very faint radial vignette / atmospheric haze.

    Parameters
    ----------
    opacity : float   Maximum haze alpha at corners [0–1].  0.04 is subtle.
    color : str       RGBA hex of the haze tint.
    """

    def __init__(self, opacity: float = 0.04, color: str = "#000000"):
        self.opacity = opacity
        self.color = color
        self._mask: np.ndarray | None = None

    def _build_mask(self, h: int, w: int) -> np.ndarray:
        cy, cx = h / 2, w / 2
        ys, xs = np.mgrid[0:h, 0:w]
        dist = np.sqrt(((xs - cx) / cx) ** 2 + ((ys - cy) / cy) ** 2)
        return np.clip(dist - 0.5, 0, 1)[..., np.newaxis] * self.opacity

    def apply(self, pixels: np.ndarray) -> np.ndarray:
        h, w = pixels.shape[:2]
        if self._mask is None or self._mask.shape[:2] != (h, w):
            self._mask = self._build_mask(h, w)
        return np.clip(pixels * (1 - self._mask), 0.0, 1.0)


class AtmosphericPass:
    """Compositor that chains bloom → grain → haze in one call."""

    def __init__(
        self,
        bloom: BloomPass | None = None,
        grain: GrainPass | None = None,
        haze: HazePass | None = None,
    ):
        self.bloom = bloom or BloomPass()
        self.grain = grain or GrainPass()
        self.haze = haze or HazePass()

    def apply(self, pixels: np.ndarray, frame: int = 0) -> np.ndarray:
        out = pixels
        if self.bloom:
            out = self.bloom.apply(out)
        if self.grain:
            out = self.grain.apply(out, frame=frame)
        if self.haze:
            out = self.haze.apply(out)
        return out
```

### Default preset for the black hole scene

```python
COSMIC_ATMOSPHERE = AtmosphericPass(
    bloom=BloomPass(threshold=0.72, sigma=16.0, strength=0.22, tint="#FFEECC"),
    grain=GrainPass(intensity=0.018),
    haze=HazePass(opacity=0.04),
)
```

Wired into `SkiaRenderer`:

```python
renderer = SkiaRenderer(clear_color=BG, atmosphere=COSMIC_ATMOSPHERE)
```

---

## Step 10 — Semantic Animation Objects (Putting It All Together)

This step is the synthesis. The goal is a single `BlackHoleScene` that internally
instantiates every system above with sensible defaults, so a caller can produce
a cinematic 12-second clip in ~10 lines.

```python
# manimlite/scenes/black_hole_scene.py

from __future__ import annotations
from manimlite import Scene, SkiaRenderer
from manimlite.shapes.black_hole import BlackHole
from manimlite.animations.cosmic_rotation import CosmicRotation
from manimlite.animations.secondary import GlowLag, LensingPulse, ParticleDrift
from manimlite.animations.camera_rig import CameraRig
from manimlite.composition.motion_layers import (
    CompositeMotion, BaseMotion, TurbulenceMotion, NoiseMotion,
)
from manimlite.composition.importance import ImportanceNode
from manimlite.rendering.atmospheric import COSMIC_ATMOSPHERE
from manimlite.styles import COSMIC_STYLE, CosmicStyleTokens
from manimlite.value import GradientOverlay
from manimlite.core import Node
import math, random


class BlackHoleScene:
    """Self-contained semantic scene.

    Instantiates materials, motion layers, camera rig, and atmospheric pass
    from a minimal set of parameters.

    Usage::

        bhs = BlackHoleScene(duration=12.0, style="interstellar")
        scene, renderer = bhs.build()
        # then pass to PyAVEncoder as usual

    Parameters
    ----------
    width, height : int   Output resolution.
    fps : float           Frame rate.
    duration : float      Clip length (s).
    style : str | CosmicStyleTokens
        "interstellar" | "mono" | "quasar" or a custom token object.
    black_hole_radius : float   Event horizon radius (px).
    disk_radius : float         Outer disk radius (px).
    disk_turns : float          Full disk rotations over the clip.
    camera_zoom_end : float     Final camera zoom factor.
    turbulence : float          Disk turbulence amplitude (radians).
    bloom_strength : float      Post-process bloom intensity.
    grain : float               Film grain intensity.
    """

    def __init__(
        self,
        width: int = 1280,
        height: int = 720,
        fps: float = 30.0,
        duration: float = 12.0,
        style: str | CosmicStyleTokens = "interstellar",
        black_hole_radius: float = 76.0,
        disk_radius: float = 300.0,
        disk_turns: float = 2.5,
        camera_zoom_end: float = 1.065,
        turbulence: float = 0.03,
        bloom_strength: float = 0.22,
        grain: float = 0.018,
    ):
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.style = style
        self.bh_radius = black_hole_radius
        self.disk_radius = disk_radius
        self.disk_turns = disk_turns
        self.camera_zoom_end = camera_zoom_end
        self.turbulence = turbulence
        self.bloom_strength = bloom_strength
        self.grain = grain

    def build(self) -> tuple[Scene, SkiaRenderer]:
        CX, CY = self.width / 2.0, self.height / 2.0
        BG = (8, 10, 22)

        scene = Scene(width=self.width, height=self.height,
                      fps=self.fps, duration=self.duration)

        # Background gradient
        scene.add_node(GradientOverlay(
            x=0.0, y=0.0,
            width=float(self.width), height=float(self.height),
            angle_rad=math.radians(128.0),
            stops=((0.0, "#0A1628"), (0.55, "#060D18"), (1.0, "#000000")),
        ))

        # Star field (low importance → slight blur)
        stars = ImportanceNode(importance=0.2, x=0.0, y=0.0)
        stars.add(_star_field(self.width, self.height, CX, CY))
        scene.add_node(stars)

        # Black hole (high importance → full brightness / contrast)
        bh_root = ImportanceNode(importance=1.0, x=CX, y=CY)
        bh = BlackHole(
            radius=self.bh_radius,
            disk_radius=self.disk_radius,
            style=self.style,
        )
        bh_root.add(bh)
        scene.add_node(bh_root)

        # Primary disk motion: base + turbulence + noise drift
        speed = self.disk_turns / self.duration
        disk_motion = CompositeMotion([
            BaseMotion(angular_velocity=speed),
            TurbulenceMotion(amplitude=self.turbulence),
            NoiseMotion(amp_x=2.0, amp_y=0.8, freq=0.06),
        ])
        scene.add_animation(0.0, self.duration, bh_root, disk_motion)

        # Secondary: glow lags, lensing pulses
        scene.add_animation(0.0, self.duration, bh._photon_ring_node,
                             GlowLag(lag=0.12,
                                     parent_rotation_fn=disk_motion.sample))
        scene.add_animation(0.0, self.duration, bh._lensed_arcs_node,
                             LensingPulse(freq=0.75, amp=0.06))

        # Camera rig
        rig = CameraRig(
            target=bh_root,
            zoom_start=1.0,
            zoom_end=self.camera_zoom_end,
            inertia=0.9,
            drift_amp=1.0,
        )
        scene.add_animation(0.0, self.duration, scene.root, rig)

        # Atmospheric renderer
        from manimlite.rendering.atmospheric import AtmosphericPass, BloomPass, GrainPass, HazePass
        atmosphere = AtmosphericPass(
            bloom=BloomPass(threshold=0.72, sigma=16.0, strength=self.bloom_strength),
            grain=GrainPass(intensity=self.grain),
            haze=HazePass(opacity=0.04),
        )
        renderer = SkiaRenderer(clear_color=BG, atmosphere=atmosphere)

        return scene, renderer
```

### Caller — 10-line recipe

```python
# examples/recipes/interstellar_black_hole_v2.py

import sys
from pathlib import Path
from manimlite.export import PyAVEncoder
from manimlite.scenes.black_hole_scene import BlackHoleScene

bhs = BlackHoleScene(
    duration=12.0,
    style="interstellar",
    turbulence=0.03,
    bloom_strength=0.22,
)
scene, renderer = bhs.build()

out = Path(__file__).with_suffix(".mp4")
encoder = PyAVEncoder(scene=scene, output_path=out, renderer=renderer,
                      linear_timeline=True)
result = encoder.encode(verbose=True)
print(f"Output: {result} ({result.stat().st_size:,} bytes)", file=sys.stderr)
```

---

## Implementation Roadmap

| Phase | Deliverable | Key files |
|-------|-------------|-----------|
| 1 | Material system + canonical library | `manimlite/materials.py` |
| 2 | Shape grammar (`DiskBand`, `AccretionDisk`, `PhotonRing`, `EventHorizon`, `BlackHole`) | `manimlite/shapes/` |
| 3 | `DistortedEllipse` + `_perlin_1d` | `manimlite/shapes/distorted_ellipse.py` |
| 4 | Style tokens + three built-in presets | `manimlite/styles.py` |
| 5 | `CosmicRotation` animation | `manimlite/animations/cosmic_rotation.py` |
| 6 | Secondary motion: `GlowLag`, `LensingPulse`, `ParticleDrift` | `manimlite/animations/secondary.py` |
| 7a | Motion layer system: `BaseMotion`, `TurbulenceMotion`, `InertiaMotion`, `NoiseMotion`, `CompositeMotion` | `manimlite/composition/motion_layers.py` |
| 7b | Importance system: `ImportanceNode` | `manimlite/composition/importance.py` |
| 8 | `CameraRig` with inertia + drift | `manimlite/animations/camera_rig.py` |
| 9 | `BloomPass`, `GrainPass`, `HazePass`, `AtmosphericPass` | `manimlite/rendering/atmospheric.py` |
| 10 | `BlackHoleScene` semantic object | `manimlite/scenes/black_hole_scene.py` |

---

## Summary

The ten steps form a layered architecture:

```
Layer 0  Raw geometry        Ellipse, Arc, Line (existing)
Layer 1  Materials           Material, canonical library
Layer 2  Semantic shapes     DiskBand → AccretionDisk → BlackHole
Layer 3  Distortion          DistortedEllipse with time-varying noise
Layer 4  Styling             CosmicStyleTokens, style presets
Layer 5  Primary motion      CosmicRotation (speed + turbulence + wobble)
Layer 6  Secondary motion    GlowLag, LensingPulse, ParticleDrift
Layer 7  Composition         MotionLayer stack + ImportanceNode
Layer 8  Camera              CameraRig (inertia + drift + zoom)
Layer 9  Atmosphere          Bloom + Grain + Haze (post-process)
Layer 10 Semantic scenes     BlackHoleScene (single-object API)
```

Each layer is independent and backward compatible. You can adopt them one at a time
without breaking the existing recipe.